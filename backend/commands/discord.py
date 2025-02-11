import discord
from utils.messaging import send_to_discord, send_to_discord_user
from utils.helpers import StateHelper, ContextHelper, load_json
from datetime import datetime, timedelta, timezone

async def lookup_access(ctx, hours: int):
  context = ContextHelper(ctx)
  await context.sys_channel.send("lookup_access() called")

  if ctx.guild:
    guild = ctx.guild
    await context.sys_channel.send(f"Guild: {guild.id} {guild.name}")
  else:
    await context.sys_channel.send("No guild...")
    return
  channels = await guild.fetch_channels()
  
  await context.sys_channel.send(f"Channels: {channels}")
  member = guild.get_member(ctx.user.id)
  if member is None:
    try:
      member = await guild.fetch_member(ctx.user.id)
    except Exception as e:
      await context.sys_channel.send(f"Error fetching member with ID: {ctx.user.id}: {e}")
      return

  for channel in channels:
    perms = channel.permissions_for(member)
    if perms.view_channel:
      await _summarize(ctx, channel, hours)

async def summarize(ctx, *args):
  context = ContextHelper(ctx)
  await context.sys_channel.send("summarize() called")

  hours = 8
  index_all = False
  if args[0].lower() == "all":
    await context.sys_channel.send("Found ALL")
    index_all = True
    if len(args) > 1 and args[1].isdigit():
      await context.sys_channel.send("Found hours")
      hours = int(args[1])
  elif args[0].isdigit():
    await context.sys_channel.send("Found only hours")
    hours = int(args[0])
  
  if index_all:
    await lookup_access(ctx, hours)
  else:
    await _summarize(ctx, ctx.channel, hours)

#  Collect messages up to a max token limit or given hours.
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
  await context.sys_channel.send(f"Summarize called for {ctx.author.name}. {len(messages)} messages collected. {total_tokens} tokens used.")

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