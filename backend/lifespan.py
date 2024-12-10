import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from services.discord_bot import DiscordBot
from services.openai_client import init_openai_client
#from services.lumaai_client import init_lumaai_client
from services.blob_storage import get_container_client
from utils.async_singleton import AsyncSingleton

@asynccontextmanager
async def lifespan(app: FastAPI):
  discord_bot = await DiscordBot.create(app)
  app.state.openai_client = AsyncSingleton(init_openai_client)
  app.state.container_client = AsyncSingleton(get_container_client)
  asyncio.get_event_loop().create_task(discord_bot.start_bot())
  yield

  #bot = await init_discord_bot()  
  #bot.app = app
  #app.state.discord_bot = bot
  #setup_bot_routes(bot)
  #openai = await init_openai_client()
  #app.state.openai_client = openai
  #lumaai = await init_lumaai_client()
  #app.state.lumaai_client = lumaai
  #container = await get_container_client()
  #app.state.container_client = container


  #bot_task = loop.create_task(start_discord_bot(bot))
  #try:
  #  yield
  #finally:
  #  bot.close()
  #  bot_task.cancel()
