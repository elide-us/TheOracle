import discord, tiktoken
from utils.messaging import send_to_discord, send_to_discord_user
from utils.helpers import StateHelper, load_json
from datetime import datetime, timedelta, timezone

#  Collect messages up to a max token limit or given hours.
async def summarize(ctx, hours: int = 1):
  state = StateHelper.from_context(ctx)

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
  await ctx.author.send(f"Collected {len(messages)} messages for summarization.")
  await state.sys_channel.send(f"Summarize called for {ctx.author.name}. {len(messages)} messages collected. {msg_tokens} tokens used.")

  return full_text

# Looks up the assistant details and submits the prompt to OpenAI
async def handle_text_generate(ctx, command_str, output):
  state = StateHelper.from_context(ctx)
  client = state.openai
  
  split = command_str.split(" ")
  key = split[0]
  prompt = " ".join(split[1:])

  json = await load_json("data_assistants.json")
  if not json:
    await state.sys_channel.send("Error loading assistant data.")
    return

  assistant = json[key]
  if not assistant:
    await state.sys_channel.send(f"Error loading assistant: {key} not found.")
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
    await state.sys_channel.send(f"Error communicating with OpenAI: {str(e)}")
    return
  
  response_text = completion.choices[0].message.content

  if output == "user":
    await send_to_discord_user(ctx.author, response_text)
  elif output == "channel":
    await send_to_discord(ctx.channel, response_text)
  else:
    await state.sys_channel.send("Undefined output")
    return

# Used by the AsyncBufferWriter to send downloads to discord
async def write_buffer_to_discord(buffer, state: StateHelper, filename: str):
  safe_filename = filename.replace(" ", "_")
  buffer.seek(0)
  await state.out_channel.send(file=discord.File(fp=buffer, filename=safe_filename))