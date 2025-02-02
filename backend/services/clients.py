import asyncpg
from openai import AsyncOpenAI
from lumaai import AsyncLumaAI, LumaAI
from azure.storage.blob.aio import BlobServiceClient
from services.env import get_discord_token, get_openai_token, get_lumaai_token
from services.env import cdn_connection_string, cdn_container_name
from services.env import db_connection_string

async def init_openai_client():
  token = get_openai_token()
  return AsyncOpenAI(api_key=token)

async def init_lumaai_client():
  token = get_lumaai_token()
  return LumaAI(auth_token=token)

async def init_storage_client():
  container = cdn_container_name()
  bsc = BlobServiceClient.from_connection_string(cdn_connection_string())
  client = bsc.get_container_client(container)
  client.container_name = container
  return client

async def init_discord_bot(bot):
  token = get_discord_token()
  await bot.start(token)

async def init_database_pool():
  pool = await asyncpg.create_pool(
    dsn=db_connection_string(),
  )
  return pool