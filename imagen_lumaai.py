import re
import asyncio, aiohttp, aiofiles
from imagen_base import LUMAAI, LUMAFADES

async def a_download_generation(video_url, filename):
  async with aiohttp.ClientSession() as session:
    #async with session.get(video_url, stream=True) as response:
    async with session.get(video_url) as response:
      if response.status == 200:
        file_path = f"{filename}.mp4"
        async with aiofiles.open(file_path, "wb") as file:
          await file.write(await response.read())
        print(f"{file_path} downloaded successfully.")
      else:
        print(f"Failed to download {file_path}. Status: {response.status}")

# Keys: fades (This is not implemented, just an idea for templating the prompts for Luma)
async def a_get_lumacuts(key: str) -> list:
  """
  Loads a particular set of cut templates from lumacuts.json.
  """
  cuts_data = await LUMAFADES.get()
  if key not in cuts_data:
    raise ValueError(f"Key '{key}' not found in JSON file.")
  cuts = cuts_data[key]
  for cut in cuts:
    print(f"{cut["name"]}")
  return cuts

def is_url(asset):
  return isinstance(asset, str) and asset.startswith("https:")

def is_valid_guid(guid):
  guid_regex = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
  )
  return isinstance(guid, str) and guid_regex.match(guid)

async def a_get_keyframes(start_asset, end_asset):
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

# prompt="Orbit right",
# prompt="Orbit left",
# prompt="Pan right",
# prompt="Pan left",
# prompt="Push in",
# prompt="Pull out",
async def a_generate_video(prompt, start_asset, end_asset, channel):
  client = await LUMAAI.get()
  keyframes = await a_get_keyframes(start_asset, end_asset)

  generation = client.generations.create(
    aspect_ratio="16:9",
    loop="false",
    prompt=prompt,
    keyframes=keyframes
  )

  while (generation := client.generations.get(id=generation.id)).state != "completed":
    if generation.state == "failed":
      await channel.send(f"Generation failed: {generation.failure_reason}.")
    if channel:
      await channel.send(f"Dreaming... current state: {generation.state}.")
    await asyncio.sleep(5)

  video_url = generation.assets.video
  filename = generation.id

  if channel:
    await channel.send(f"Generation URL: {video_url}, Generation ID: {filename}")
  await a_download_generation(video_url, filename)
