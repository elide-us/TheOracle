import re, asyncio
from utils.helpers import StateHelper, AsyncBufferWriter, DownloadRegistry
from commands.discord import write_buffer_to_discord
from commands.storage import write_buffer_to_blob

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

async def download_generation(video_url, state, filename):
  registry: DownloadRegistry = state.lumaai_downloads

  existing_task = await registry.get_task(filename)
  if existing_task:
    await existing_task
    return

  task = asyncio.create_task(_download_generation(video_url, state, filename))
  await registry.add_task(filename, task)
  
  try:
    await task
  finally:
    await registry.remove_task(filename)

async def _download_generation(video_url, state, filename):
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
      callback_url="https://elideusgroup.com/api/lumagen/callback",
      keyframes=keyframes
    )
    await state.sys_channel.send(f"Response: {response}")
  except Exception as e:
    await state.sys_channel.send(f"Exception: {e}")  
