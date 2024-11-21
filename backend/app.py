import os
import json
import discord
import threading
from flask import Flask, render_template
from discord.ext import commands
#from multiprocessing import Process

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print("Bot online.")

@bot.command(name="ai")
async def ping(ctx):
  await ctx.send("Online.")

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
  bot_thread = threading.Thread(target=run_bot)

  #flask_process = Process(target=run_flask)
  #bot_process = Process(target=run_bot)

  flask_thread.start()
  bot_thread.start()

  flask_thread.join()
  bot_thread.join()
