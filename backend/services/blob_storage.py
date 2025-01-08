from azure.storage.blob.aio import BlobServiceClient
from config import get_blob_connection_string, get_blob_container

async def get_container_client():
  conn_str = get_blob_connection_string()
  container_name = get_blob_container()
  blob_service_client = BlobServiceClient.from_connection_string(conn_str)
  container_client = blob_service_client.get_container_client(container_name)
  container_client.container_name = container_name
  return container_client

#Provision new blob storage container