import discord, asyncio
from utils.messaging import send_to_discord, send_to_discord_user
from utils.helpers import StateHelper, ContextHelper, load_json
from datetime import datetime, timedelta, timezone
from commands.postgres import database_fetch_one

# class SummaryQueue:
#   def __init__(self, delay=15):
#     self.queue = deque()
#     self.delay = delay
#     self.processing = False
#   async def add(self, func, *args, **kwargs):
#     self.queue.append((func, args, kwargs))
#     if not self.processing:
#       asyncio.create_task(self._process_queue())
#   async def _process_queue(self):
#     self.proessing = True
#     while self.queue:
#       func, args, kwargs = self.queue.popleft()
#       await func(*args, **kwargs)
#       await asyncio.sleep(self.delay)
#     self.processing = False

class SummaryQueue:
  def __init__(self, delay=15):
    self.queue = asyncio.Queue()
    self._lock = asyncio.Lock()
    self.delay = delay
    self.processing = False
    self._processing_task = None
  async def add(self, func, *args, **kwargs):
    async with self._lock:
      await self.queue.put((func, args, kwargs))
      if not self.processing:
        self.processing = True
        loop = asyncio.get_event_loop()
        self._processing_task = loop.create_task(self._process_queue())
    async def _process_queue(self):
      try:
        while not self.queue.empty():
          func, args, kwargs = await self.queue.get()
          await func(*args, **kwargs)
          await asyncio.sleep(self.delay)
        self.processing = False
      except asyncio.CancelledError:
        raise
      finally:
        async with self._lock:
          self.processing = False

# Function to look up a user's guild and then check their channel read access
# and summarize only channels they have access to
async def lookup_access(ctx, hours: int):
  context = ContextHelper(ctx)
  await context.sys_channel.send("lookup_access() called")

  if ctx.guild:
    guild = ctx.guild
    await context.sys_channel.send(f"Guild: {guild.id} {guild.name}")
  else:
    await context.sys_channel.send("No guild...")
    return None

  results = []
  for channel in guild.text_channels:
    await ctx.author.send(f"Collecting messages in channel {channel.name}")
    perms = channel.permissions_for(ctx.author)
    if perms.view_channel:
      result = await context.app.state.openai_queue.add(_summarize, ctx, channel, hours)
      results.append(result)
      # return await _summarize(ctx, channel, hours)

# New entry point for summarize that captures and extracts the "all" argument
async def summarize(ctx, *args):
  hours = 8
  index_all = False
  if args[0].lower() == "all":
    index_all = True
    if len(args) > 1 and args[1].isdigit():
      hours = int(args[1])
  elif args[0].isdigit():
    hours = int(args[0])
  
  if index_all:
    return await lookup_access(ctx, hours)
  else:
    return await _summarize(ctx, ctx.channel, hours)

# Collect messages up to a max token limit or given hours.
async def _summarize(ctx, channel, hours: int):
  context = ContextHelper(ctx)
  await context.sys_channel.send("_summarize() called")

  max_tokens = 3800  # Hardcoded max token count
  tokenizer = context.tokenizer
  
  since = datetime.now(timezone.utc) - timedelta(hours=hours)
  message_stack = []
  total_tokens = 0

  async for msg in channel.history(limit=5000, oldest_first=False):
    msg_text = f"{msg.author.display_name}: {msg.content}"
    msg_tokens = len(tokenizer.encode(msg_text))

    if msg.created_at < since or (total_tokens + msg_tokens) > max_tokens:
      break  # Stop collecting when limit is reached

    message_stack.append(msg_text)  # Push onto stack
    total_tokens += msg_tokens

  messages = message_stack[::-1]  # Unwind stack into chronological order

  if not messages:
    await ctx.author.send("No messages found in the given time range.")
    return
  
  full_text = " ".join(messages)
  await ctx.author.send(f"Collected {len(messages)} messages for summarization.")
  await context.sys_channel.send(f"Summarize {hours} hours history on channel {ctx.guild.name}:{ctx.channel.name} called for {ctx.author.name}. {len(messages)} messages collected, {total_tokens} tokens used.")

  return full_text

# Looks up the assistant details and submits the prompt to OpenAI
async def handle_text_generate(ctx, command_str, output):
  context = ContextHelper(ctx)
  client = context.openai
  
  split = command_str.split(" ")
  key = split[0]
  prompt = " ".join(split[1:])

  json = await load_json("data_assistants.json")
  if not json:
    await context.sys_channel.send("Error loading assistant data.")
    return

  assistant = json[key]
  if not assistant:
    await context.sys_channel.send(f"Error loading assistant: {key} not found.")
    return

  ## await debug.send(f"Sending prompt to OpenAI: {prompt}")
  try:
    completion = await client.chat.completions.create(
      model=assistant["model"],
      max_tokens=assistant["max_tokens"],
      messages=[
        {"role": "system", "content": assistant["role"]},
        {"role": "user", "content": prompt}
      ]
    )
    response_text = completion.choices[0].message.content
  except Exception as e:
    await context.sys_channel.send(f"Error communicating with OpenAI: {str(e)}")
    return
  
  response_text = completion.choices[0].message.content

  if output == "user":
    await send_to_discord_user(ctx.author, response_text)
  elif output == "channel":
    await send_to_discord(ctx.channel, response_text)
  else:
    await context.sys_channel.send("Undefined output")
    return

# Used by the AsyncBufferWriter to send downloads to discord
async def write_buffer_to_discord(buffer, state: StateHelper, filename: str):
  safe_filename = filename.replace(" ", "_")
  buffer.seek(0)
  await state.out_channel.send(file=discord.File(fp=buffer, filename=safe_filename))

async def handle_command_assistants(ctx, *args):
  context = ContextHelper(ctx)
  query = """
    SELECT jsonb_agg(name) AS names FROM assistants;
  """
  return await database_fetch_one(context.pool, query, *args)


