import os
import discord
from discord.ext import commands
# from openai import AsyncOpenAI
# from lumaai import LumaAI
from AsyncSingleton import AsyncSingleton # , a_load_json

# General config.json dictionary with various values for local run
# CONFIG = AsyncSingleton(lambda: a_load_json("config.json"))
# TEMPLATES = AsyncSingleton(lambda: a_load_json("templates.json"))
# DATA = AsyncSingleton(lambda: a_load_json("data.json"))

# DATA_TEMPLATES = AsyncSingleton(lambda: a_load_json("data_templates.json"))
# DATA_PALETTES = AsyncSingleton(lambda: a_load_json("data_palettes.json"))
# DATA_COMPOSITIONS = AsyncSingleton(lambda: a_load_json("data_compositions.json"))

# async def a_load_lumafades() -> list:
#   data = DATA.get()
#   lumafades = data["lumafades"]
#   return lumafades

# async def a_load_annotations() -> list:
#   data = DATA.get()
#   annotations = data["annotations"]
#   return annotations

# async def a_load_ttslines() -> list:
#   data = DATA.get()
#   ttslines = data["ttslines"]
#   return ttslines

# LUMAFADES = AsyncSingleton(lambda: a_load_lumafades())
# ANNOTATIONS = AsyncSingleton(lambda: a_load_annotations())
# TTSLINES = AsyncSingleton(lambda: a_load_ttslines())

# async def a_get_openai_token() -> str:
#   """
#   Gets the OpenAI bearer token from the environment or config.json.
#   """
#   secret = os.getenv('OPENAI_SECRET')
#   if secret:
#     return secret
#   else:
#     config = await CONFIG.get()
#     return config["tokens"]["openai"]

# async def a_init_openai():
#   """
#   Creates and initializes the OpenAI client.
#   """
#   print("Initializing OpenAI client.")
#   token = await a_get_openai_token()
#   return AsyncOpenAI(api_key=token)

# OPENAI = AsyncSingleton(a_init_openai)

# async def a_get_lumaai_token() -> str:
#   """
#   Gets the LumaAI API bearer token from the environment or config.json.
#   """
#   secret = os.getenv('LUMAAI_SECRET')
#   if secret:
#     return secret
#   else:
#     config = await CONFIG.get()
#     return config["tokens"]["lumaai"]

# async def a_init_lumaai():
#   """
#   Creates and initializes the LumaAI client.
#   """
#   print("Initializing LumaAI client.")
#   token = await a_get_lumaai_token()
#   return LumaAI(auth_token=token)

# LUMAAI = AsyncSingleton(a_init_lumaai)

async def a_init_discord():
  intents = discord.Intents.default()
  intents.messages = True
  intents.message_content = True
  bot = commands.Bot(command_prefix='!', intents=intents)
  return bot

async def a_get_discord_token() -> str:
  secret = os.getenv('DISCORD_SECRET')
  if not secret:
    raise RuntimeError("ERROR: DISCORD_SECRET missing.")
  else:
    return secret

async def a_get_discord_channel() -> int:
  channel = int(os.getenv('DISCORD_CHANNEL'))
  if not channel:
    raise RuntimeError("ERROR: DISCORD_CHANNEL missing.")
  else:
    return channel

DISCORD = AsyncSingleton(a_init_discord)
DISCORD_TOKEN = AsyncSingleton(a_get_discord_token)
DISCORD_CHANNEL = AsyncSingleton(a_get_discord_channel)
