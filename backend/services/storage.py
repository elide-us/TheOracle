from azure.storage.blob.aio import BlobServiceClient
from conf.env import cdn_connection_string, cdn_container_name

async def init_container_client():
  container = cdn_container_name()
  bsc = BlobServiceClient.from_connection_string(cdn_connection_string())
  client = bsc.get_container_client(container)
  client.container_name = container
  return client

#Provision new blob storage container