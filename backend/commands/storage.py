from utils.helpers import StateHelper
from azure.storage.blob import ContentSettings
import mimetypes

async def write_buffer_to_blob(buffer, state: StateHelper, filename: str):
  safe_filename = filename.replace(" ", "_")
  buffer.seek(0)
  client = state.storage
  content_type, _ = mimetypes.guess_type(safe_filename)
  if content_type is None:
    content_type = "application/octet-stream"
  await client.upload_blob(
    data=buffer,
    name=safe_filename,
    overwrite=True,
    content_settings=ContentSettings(content_type=content_type)
  )