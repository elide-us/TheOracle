import aiofiles, json
from typing import Any
from azure.storage.blob.aio import BlobServiceClient
from config.env import cdn_connection_string, cdn_container_name

async def init_storage_client():
  container = cdn_container_name()
  bsc = BlobServiceClient.from_connection_string(cdn_connection_string())
  client = bsc.get_container_client(container)
  client.container_name = container
  return client

async def load_json(file_path: str) -> Any:
  try:
    async with aiofiles.open(file_path, mode='r') as file:
      return json.loads(await file.read())
  except FileNotFoundError:
    return None

#Provision new blob storage container