import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.env import get_jwt_secret, get_ms_app_id, get_discord_channel, get_debug_ch, get_image_ch, get_video_ch, get_audio_ch, get_chat_ch
from services.discord import init_discord_bot, setup_bot_routes, start_discord_bot
from services.storage import init_storage_client
from services.postgres import init_database_pool
from services.openai import init_openai_client
from services.lumaai import init_lumaai_client
from services.auth import fetch_ms_jwks_uri, fetch_ms_jwks

@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await init_discord_bot()
  bot.sys_channel = get_discord_channel()
  bot.debug_channel = bot.get_channel(get_debug_ch())
  bot.image_channel = bot.get_channel(get_image_ch())
  bot.video_channel = bot.get_channel(get_video_ch())
  bot.audio_channel = bot.get_channel(get_audio_ch())
  bot.chat_channel = bot.get_channel(get_chat_ch())
  bot.app = app
  app.state.discord_bot = bot

  app.state.jwt_secret = get_jwt_secret()
  app.state.jwt_algorithm_rs256 = "RS256"
  app.state.jwt_algorithm_hs256 = "HS256"
  app.state.ms_app_id = get_ms_app_id()
  app.state.ms_jwks_uri = await fetch_ms_jwks_uri()
  app.state.ms_jwks = await fetch_ms_jwks(app.state.ms_jwks_uri)

  app.state.openai_client = await init_openai_client()
  app.state.lumaai_client = await init_lumaai_client()
  app.state.theoraclesa_client = await init_storage_client()
  app.state.theoraclegp_pool = await init_database_pool()

  setup_bot_routes(bot)
  loop = asyncio.get_event_loop()
  bot_task = loop.create_task(start_discord_bot(bot))

  try:
    yield
  finally:
    await bot.close()
    bot_task.cancel()

################################################################################
## Old code samples for luma and co-routine
################################################################################

# from lumaai import LumaAI
# import asyncio, aiohttp, aiofiles, re

# async def a_download_generation(video_url, filename):
#   async with aiohttp.ClientSession() as session:
#     #async with session.get(video_url, stream=True) as response:
#     async with session.get(video_url) as response:
#       if response.status == 200:
#         file_path = f"{filename}.mp4"
#         async with aiofiles.open(file_path, "wb") as file:
#           await file.write(await response.read())
#         print(f"{file_path} downloaded successfully.")
#       else:
#         print(f"Failed to download {file_path}. Status: {response.status}")

# # Keys: fades (This is not implemented, just an idea for templating the prompts for Luma)
# async def a_get_lumacuts(key: str) -> list:
#   """
#   Loads a particular set of cut templates from lumacuts.json.
#   """
#   cuts_data = {}
#   if key not in cuts_data:
#     raise ValueError(f"Key '{key}' not found in JSON file.")
#   cuts = cuts_data[key]
#   for cut in cuts:
#     print(f"{cut["name"]}")
#   return cuts

# def is_url(asset):
#   return isinstance(asset, str) and asset.startswith("https:")

# def is_valid_guid(guid):
#   guid_regex = re.compile(
#     r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
#   )
#   return isinstance(guid, str) and guid_regex.match(guid)

# async def a_get_keyframes(start_asset, end_asset):
#   keyframes = {}

#   if start_asset:
#     if is_url(start_asset):
#       keyframes["frame0"] = {
#         "type": "image",
#         "url": start_asset
#       }
#     elif is_valid_guid(start_asset):
#       keyframes["frame0"] = {
#         "type": "generation",
#         "id": start_asset
#       }

#   if end_asset:
#     if is_url(end_asset):
#       keyframes["frame1"] = {
#         "type": "image",
#         "url": end_asset
#       }
#     elif is_valid_guid(end_asset):
#       keyframes["frame1"] = {
#         "type": "generation",
#         "id": end_asset
#       }

#   return keyframes

# # prompt="Orbit right",
# # prompt="Orbit left",
# # prompt="Pan right",
# # prompt="Pan left",
# # prompt="Push in",
# # prompt="Pull out",
# async def a_generate_video(prompt, start_asset, end_asset, channel):
#   client = LumaAI()
#   keyframes = await a_get_keyframes(start_asset, end_asset)

#   generation = client.generations.create(
#     aspect_ratio="16:9",
#     loop="false",
#     prompt=prompt,
#     keyframes=keyframes
#   )

#   while (generation := client.generations.get(id=generation.id)).state != "completed":
#     if generation.state == "failed":
#       await channel.send(f"Generation failed: {generation.failure_reason}.")
#     if channel:
#       await channel.send(f"Dreaming... current state: {generation.state}.")
#     await asyncio.sleep(5)

#   video_url = generation.assets.video
#   filename = generation.id

#   if channel:
#     await channel.send(f"Generation URL: {video_url}, Generation ID: {filename}")
#   await a_download_generation(video_url, filename)

# async def co_produce_prompt(template_key, palette_key, channel):
#   identifier = f"{template_key}_{palette_key}"
#   template = await a_get_template(template_key)
#   palette = await a_get_palette(palette_key)
#   palette_dict = await a_make_dict(palette)
#   prompt = await a_format_template(template, palette_dict)
#   filename = await a_generate_filename(identifier)
#   yield prompt, filename, channel

# async def co_consume_prompt(producer_coroutine):
#   async for prompt, filename, channel in producer_coroutine:
#     image_url = await a_generate_image(prompt)
#     await a_download_image(image_url, filename, channel)

# async def co_run_images(template_key, palette_key, channel):
#   producer_coroutine = co_produce_prompt(template_key, palette_key, channel)
#   await co_consume_prompt(producer_coroutine)
