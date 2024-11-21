import os
import json
import discord
import threading
from flask import Flask
from discord.ext import commands

DISCORD_TOKEN =  os.getenv('DISCORD_TOKEN')
WEBHOOK_ID = 1308553886868574409

WEBHOOK_URL = 'https://discordapp.com/api/webhooks/{WEBHOOK_ID}/{DISCORD_TOKEN}'

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello, World!"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print("Bot online")

@bot.command
async def ping(ctx):
  await ctx.send("Pong!")

def s_load_json(file_path):
  with open(file_path, "r") as file:
    data = json.load(file)
  return data

def run_flask():
  app.run(host="0.0.0.0", port=80)

def run_bot():
  discord_key = os.getenv('DISCORD_SECRET')
  if not discord_key:
    raise ValueError("Missing key")
  bot.run(discord_key)

if __name__ == '__main__':
  flask_thread = threading.Thread(target=run_flask)
  flask_thread.start()

  run_bot()

