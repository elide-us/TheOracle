import re, io
from utils.helpers import StateHelper, AsyncBufferWriter
from commands.discord import write_buffer_to_discord
from commands.storage import write_buffer_to_blob

## THIS CODE IS UNFINISHED AND MUST NOT BE CALLED ##

def is_url(asset):
  return isinstance(asset, str) and asset.startswith("https:")

def is_valid_guid(guid):
  guid_regex = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
  )
  return isinstance(guid, str) and guid_regex.match(guid)

async def get_keyframes(start_asset, end_asset):
  keyframes = {}

  if start_asset:
    if is_url(start_asset):
      keyframes["frame0"] = {
        "type": "image",
        "url": start_asset
      }
    elif is_valid_guid(start_asset):
      keyframes["frame0"] = {
        "type": "generation",
        "id": start_asset
      }

  if end_asset:
    if is_url(end_asset):
      keyframes["frame1"] = {
        "type": "image",
        "url": end_asset
      }
    elif is_valid_guid(end_asset):
      keyframes["frame1"] = {
        "type": "generation",
        "id": end_asset
      }

  return keyframes

# This won't work in this form, needs to follow the ByteIO download to memory and then send to Discord/Storage Account pattern.
async def download_generation(video_url, state, filename):
  async with AsyncBufferWriter(video_url) as buffer:
    await write_buffer_to_blob(buffer, state, filename)
    await write_buffer_to_discord(buffer, state, filename)

async def generate_video(ctx, start_asset, end_asset, prompt):
  state = StateHelper.from_context(ctx)
  client = state.lumaai

  keyframes = await get_keyframes(start_asset, end_asset)

  try:
    response = await client.generations.create(
      aspect_ratio="16:9",
      loop="false",
      prompt=prompt,
      callback_url="https://elideusgroup.com/api/lumaai",
      keyframes=keyframes
    )
    await state.sys_channel.send(f"Response: {response}")
  except Exception as e:
    await state.sys_channel.send(f"Exception: {e}")  
