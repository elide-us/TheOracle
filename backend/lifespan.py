import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from services.discord_bot import init_discord_bot, start_discord_bot, get_discord_channel_id
from services.openai_client import init_openai_client
from services.blob_storage import get_container_client
from routes.bot import setup_bot_commands

@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await init_discord_bot()
  openai = await init_openai_client()
  #lumaai = await init_lumaai_client()
  container = await get_container_client()

  bot.app = app
  app.state.discord_bot = bot
  app.state.openai_client = openai
  app.state.container_client = container

  bot_channel_id = await get_discord_channel_id()
  setup_bot_commands(bot, bot_channel_id)

  loop = asyncio.get_event_loop()
  bot_task = loop.create_task(start_discord_bot(bot))

  try:
    yield
  finally:
    channel = bot.get_channel(bot_channel_id)
    if channel:
      await channel.send("TheOracleGPT Shutting down.")
    await bot.close()
    bot_task.cancel()
