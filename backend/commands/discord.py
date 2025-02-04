import discord, tiktoken
from utils.messaging import send_to_discord, send_to_discord_user
from utils.helpers import StateHelper, load_json
from datetime import datetime, timedelta, timezone

async def summarize(ctx, hours: int = 1):
  """Collect messages up to a max token limit or given hours."""
  max_tokens = 3800  # Hardcoded max token count
  tokenizer = tiktoken.get_encoding("cl100k_base")
  
  since = datetime.now(timezone.utc) - timedelta(hours=hours)
  message_stack = []
  total_tokens = 0

  async for msg in ctx.channel.history(limit=5000, oldest_first=False):
    msg_text = f"{msg.author.display_name}: {msg.content}"
    msg_tokens = len(tokenizer.encode(msg_text))

    if msg.created_at < since or (total_tokens + msg_tokens) > max_tokens:
      break  # Stop collecting when limit is reached

    message_stack.append(msg_text)  # Push onto stack
    total_tokens += msg_tokens

  messages = list(reversed(message_stack))  # Unwind stack into chronological order

  if not messages:
    await ctx.send("No messages found in the given time range.")
    return
  
  full_text = " ".join(messages)
  await ctx.send(f"Collected {len(messages)} messages for summarization.")

  return full_text

async def handle_text_generate(ctx, command_str, output):
  app = ctx.bot.app
  channel = ctx.channel
  user = ctx.author
  client = app.state.openai_client
  
  split = command_str.split(" ")
  key = split[0]
  prompt = " ".join(split[1:])

  json = await load_json("data_assistants.json")
  if not json:
    await channel.send("Error loading assistant data.")
    return

  assistant = json[key]
  if not assistant:
    await channel.send(f"Error loading assistant: {key} not found.")
    return

  ## await channel.send(f"Sending prompt to OpenAI: {prompt}")
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
    await channel.send(f"Error communicating with OpenAI: {str(e)}")
    return
  
  response_text = completion.choices[0].message.content

  if output is "user":
    await send_to_discord_user(user, response_text)
  elif output is "channel":
    await send_to_discord(channel, response_text)
  else:
    await channel.send("Undefined output")
    return

async def write_buffer_to_discord(buffer, state: StateHelper, filename):
  buffer.seek(0)
  await state.channel.send(file=discord.File(fp=buffer, filename=filename))