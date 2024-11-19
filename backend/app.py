import os
import json
import discord

DISCORD_SECRET = os.getenv('DISCORD_SECRET')
CHANNEL_ID = 1306414351598747709
LOCAL = False

def s_load_json(file_path):
  with open(file_path, "r") as file:
    data = json.load(file)
  return data

def get_discord_key():
  print("get_discord_key()")
  if LOCAL is True:
    config = s_load_json("config.json")
    return config["discord_key"]
  else:
    return DISCORD_SECRET

def get_discord():
  print("get_discord()")
  intents = discord.Intents.default()
  intents.messages = True
  intents.message_content = True
  bot = discord.Client(intents=intents)
  return bot

def run_discord_bot():
  bot = get_discord()
  key = get_discord_key()

  @bot.event
  async def on_ready():
    print("on_ready()")

  @bot.event
  async def on_message(message):
    print("on_message()")
    if message.author == bot.user:
      return
    if message.content.startswith("!image"):
      response_text = message.content[len("!image"):].strip()
      await message.channel.send(response_text)

  print("Starting bot")
  bot.run(token=key)

run_discord_bot()
