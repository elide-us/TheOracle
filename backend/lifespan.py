import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from services.discord_bot import init_discord_bot, start_discord_bot, get_discord_channel_id
from services.openai_client import init_openai_client
#from services.lumaai_client import init_lumaai_client
from services.blob_storage import get_container_client
from routes.bot import setup_bot_commands

@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await init_discord_bot()
  bot.sys_channel = await get_discord_channel_id()
  bot.app = app

  app.state.discord_bot = bot

  openai = await init_openai_client()
  app.state.openai_client = openai

  #lumaai = await init_lumaai_client()

  container = await get_container_client()
  app.state.container_client = container

  setup_bot_commands(bot)

  loop = asyncio.get_event_loop()
  bot_task = loop.create_task(start_discord_bot(bot))

  try:
    yield
  finally:
    await bot.close()
    bot_task.cancel()
