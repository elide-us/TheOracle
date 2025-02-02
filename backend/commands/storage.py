from utils.helpers import StateHelper

async def write_buffer_to_blob(buffer, state: StateHelper, filename):
  buffer.seek(0)
  client = state.storage
  await client.upload_blob(data=buffer, name=filename, overwrite=True)