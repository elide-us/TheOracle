import os
import asyncio
import discord
from discord.ext import commands
from openai import AsyncOpenAI
# from lumaai import LumaAI
from contextlib import asynccontextmanager
from fastapi import FastAPI

from AsyncSingleton import AsyncSingleton
#from imagen_openai import a_generate_text

async def a_init_discord():
  intents = discord.Intents.default()
  intents.messages = True
  intents.message_content = True
  bot = commands.Bot(command_prefix='!', intents=intents)
  return bot
async def a_get_discord_token() -> str:
  secret = os.getenv('DISCORD_SECRET')
  if not secret:
    raise RuntimeError("ERROR: DISCORD_SECRET missing.")
  else:
    return secret
async def a_get_discord_channel() -> int:
  channel = int(os.getenv('DISCORD_CHANNEL'))
  if not channel:
    raise RuntimeError("ERROR: DISCORD_CHANNEL missing.")
  else:
    return channel

async def a_get_openai_token() -> str:
  secret = os.getenv('OPENAI_SECRET')
  if not secret:
    raise RuntimeError("ERROR: OPENAI_SECRET missing.")
  else:
    return secret
async def a_init_openai():
  token = await a_get_openai_token()
  return AsyncOpenAI(api_key=token)

OPENAI = AsyncSingleton(a_init_openai)

async def a_generate_text(prompt: str) -> str:
  print("Sending text prompt to OpenAI.")
  client = await OPENAI.get()
  completion = await client.chat.completions.create(
    model="chatgpt-4o-latest",
    max_completion_tokens=50,
    messages=[
      {"role":"system","content":"You are a helpful assistant."},
      {"role":"user","content":prompt}
    ]
  )
  return completion.choices[0].message.content

async def a_handle_text_generate(args: str, channel: str):
  if len(args) < 1:
    channel.send("Text generate requires a prompt.")
  prompt = " ".join(args)
  channel.send("Starting text generation...")
  return await a_generate_text(prompt)


async def a_get_dispatcher():
  return {
    "text": {
      "generate": lambda args, channel: a_handle_text_generate(args, channel)
    },
    "image": {
      # "generate": lambda args, channel: a_handle_image_generate(args, channel)
      # ,"list": lambda args: handle_image_list(args)
      # ,"delete": lambda args: handle_image_delete(args)
    },
    "audio": {
      # "generate": lambda args, channel: a_handle_audio_generate(args, channel)
      # ,"list": lambda args: handle_audio_list(args)
      # ,"delete": lambda args: handle_audio_delete(args)

    }
    ,"video": {
      # "generate": lambda args, channel: a_handle_video_generate(args, channel)
      # ,"append": lambda args: handle_video_append(args)
      # ,"list": lambda args: handle_video_list(args)
      # ,"delete": lambda args: handle_video_delete(args)
    }
  }

async def a_parse_and_dispatch(command: str, channel: str, dispatcher):
  words = command.split()
  if len(words) < 2: # Basic input validation
    channel.send("Invalid command format. Must include <result> <action>.")
  result, action = words[0], words[1]
  args = words[2:]
  if result not in dispatcher or action not in dispatcher[result]: # Dispatch map validation
    channel.send(f"Unknown command: {result} {action}")
  response = await dispatcher[result][action](args, channel)
  return response

# Async context manager for FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await a_init_discord()
  bot_token = await a_get_discord_token()
  bot_channel = await a_get_discord_channel()

  bot_dispatcher  = await a_get_dispatcher()

  # OPENAI = AsyncSingleton(a_init_openai)

  @bot.command(name="help")
  async def help(ctx):
    await ctx.send("I would love to help you... another time.")

  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot_channel)
    if channel:
      await channel.send("imagen Online.")

  @bot.command(name="imagen")
  async def imagen(ctx, *args):
    command_str = " ".join(args)
    try:
      channel = ctx.channel
      channel.send("Try: a_parse_and_dispatch()")
      response = await a_parse_and_dispatch(command_str, channel, bot_dispatcher)
      if response:
        await ctx.send(response)
    except ValueError as e:
      await ctx.send(f"Error: {str(e)}")
    except Exception as e:
      await ctx.send(f"An unexpected error occurred: {str(e)}")

  loop = asyncio.get_event_loop()
  bot_task = loop.create_task(bot.start(bot_token))

  try:
    yield  # Suspend context until FastAPI shuts down
  finally:
    await bot.close()
    bot_task.cancel()

# Create the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running with a Discord bot!"}
