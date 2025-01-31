import tiktoken
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from commands.tts_commands import handle_tts
from commands.discord import handle_text_generate
from services.local_json import load_json

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




def setup_bot_routes(bot: commands.Bot):
  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot.sys_channel)
    await channel.send("TheOracleGPT Online.")

  @bot.event
  async def on_guild_join(guild):
    channel = bot.get_channel(bot.sys_channel)
    if channel:
      await channel.send(f"Joined {guild.name} ({guild.id})")

  @bot.command(name="tts")
  async def tts_gen(ctx, *args):
    command_str = " ".join(args)
    response = await handle_tts(ctx, command_str)
    if response:
      await ctx.send(response)

  @bot.command(name="hello")
  async def hello(ctx):
    await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  @bot.command(name="summarize")
  async def summarize_chat(ctx, hours: int = 1):
    text = await summarize(ctx, hours)

    command_str = f"summary Summarize the following conversations: {text}"
    exception = await handle_text_generate(ctx, command_str=command_str)
    if exception:
      await ctx.send(f"Exception: {exception}")

  @bot.command(name="assistants", help="Lists the assistants available for the !chat command.")
  async def assistants(ctx, *args):
    data = await load_json("data_assistants.json")
    assistants_list = ", ".join(data.keys())
    await ctx.send(f"Available assistants: {assistants_list}")

  @bot.command(name="chat", help="Format: !chat <assistant> <Your question here.> Each assistant is tuned to provide specific expertise.")
  async def chat(ctx, *args):
    command_str = " ".join(args)
    response = await handle_text_generate(ctx, command_str)
    if response:
      await ctx.send(response)

  # @bot.command(name="video")
  # async def video_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   lumaai_client = ctx.bot.app.state.lumaai_client
  #   response = await handle_video(command_str, lumaai_client)
  #   if response:
  #     await ctx.send(response)
 
  # @bot.command(name="image")
  # async def image_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   openai_client = ctx.bot.app.state.openai_client
  #   response = await handle_image(command_str, openai_client)
  #   if response:
  #     await ctx.send(response)