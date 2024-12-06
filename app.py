import os, asyncio, discord
from discord.ext import commands
from contextlib import asynccontextmanager
from fastapi import FastAPI
from openai import AsyncOpenAI

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

# Async context manager for FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await a_init_discord()
  bot_token = await a_get_discord_token()
  bot_channel = await a_get_discord_channel()
  # openai_client = await a_init_openai()

  @bot.command(name="hello")
  async def hello(ctx):
    await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot_channel)
    if channel:
      await channel.send("TheOracleGPT Online.")

  # Do stuff with OpenAI client here...

  loop = asyncio.get_event_loop()
  bot_task = loop.create_task(bot.start(bot_token))

  try:
    yield  # Suspend context until FastAPI shuts down
  finally:
    await bot.close()
    bot_task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running with a Discord bot!"}
