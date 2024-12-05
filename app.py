import os
import asyncio
import discord
from discord.ext import commands
# from openai import AsyncOpenAI
# from lumaai import LumaAI

from contextlib import asynccontextmanager
from fastapi import FastAPI

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

# Async context manager for FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await a_init_discord()
  bot_token = await a_get_discord_token()
  bot_channel = await a_get_discord_channel()

  @bot.command(name="hello")
  async def hello(ctx):
    await ctx.send("Hello from Discord Bot!")

  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot_channel)
    if channel:
      await channel.send("imagen Online.")

  # @bot.command(name="imagen")
  # async def imagen(ctx, *args):
  #   command_str = " ".join(args)
  #   try:
  #     channel = ctx.channel
  #     response = await a_parse_and_dispatch(command_str, channel)
  #     if response:
  #       await ctx.send(response)
  #   except ValueError as e:
  #     await ctx.send(f"Error: {str(e)}")
  #   except Exception as e:
  #     await ctx.send(f"An unexpected error occurred: {str(e)}")

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
