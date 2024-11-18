import json
import requests
import asyncio
import aiofiles
import aiohttp
import discord
import threading
from datetime import time, datetime, timezone
from lumaai import LumaAI
from openai import OpenAI, AsyncOpenAI
from flask import Flask, render_template, request
import os

OPENAI_SECRET = os.getenv('OPENAI_SECRET')
DISCORD_SECRET = os.getenv('DISCORD_SECRET')
YOUR_CHANNEL_ID = 1306414351598747709

# Flask App Setup
app = Flask(__name__, static_folder='static', template_folder='templates')

# Discord Bot Setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = discord.Client(intents=intents)

@app.route('/')
def index():
  return render_template('index.html')

#Endpoint Example (Optional: Handle API tasks)
#@app.route('/process', methods=['POST'])
#def process_task():
#    data = request.json
#    # Example: Process external API task
#    result = f"Processed: {data['task']}"
#    return {"result": result}, 200

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')  # This is useful for logging/debugging.
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with the channel ID
    if channel:
        await channel.send("Hello! The bot is now online and ready to serve!")
    else:
        print("Channel not found or bot does not have access to the channel.")


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.content.startswith("!process"):
    # Example: Responding to "!process" commands
    task = message.content[9:].strip()  # Extract text after "!process"
    if task:
      # Process the task or call an endpoint
      response = f"Processing your task: {task}"
      await message.channel.send(response)
    else:
      await message.channel.send("Please provide a task after '!process'.")

############################################################

def s_load_json(file_path):
  with open(file_path, "r") as file:
    data = json.load(file)
  return data

def s_get_template(key):
  print("Getting prompt template")
  template_data = s_load_json("templates.json")
  if key not in template_data:
    raise ValueError(f"Key '{key}' not found in JSON file.")
  template = template_data[key]
  return template

def s_get_arguments(key):
  print("Getting template key map")
  argument_data = s_load_json("arguments.json")
  if key not in argument_data:
    raise ValueError(f"Key '{key}' not found in JSON file.")
  arguments = argument_data[key]
  return arguments

def s_generate_filename(arguments):
  timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
  filename = f"{timestamp}_{arguments['arg0']}_{arguments['arg1']}"
  print(f"Generated filename: {filename}.png")
  return filename

def s_generate_prompt(template, arg_set):
  print(f"Merging prompt with arguments: {arg_set}")
  return template.format(**arg_set)

def s_init_openai():
  print("Initializing OpenAI")
  config = s_load_json("config.json")
  return OpenAI(api_key=config["openai_key"])

def s_generate_image(client, prompt):
  print("Sending prompt to DALL-E-3")
  response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",
    quality="standard",
    n=1
  )
  image_url = response.data[0].url
  return image_url

def s_download_image(image_url, filename):
  print(f"Downloading {filename}.png")
  response = requests.get(image_url, stream=True)
  with open(f"{filename}.png", "wb") as file:
    file.write(response.content)

############################################################

async def co_produce_prompts(template_key, arguments_key):
  template = s_get_template(template_key)
  arguments_list = s_get_arguments(arguments_key)
  for arg_set in arguments_list:
    prompt = s_generate_prompt(template, arg_set)
    filename = s_generate_filename(arg_set)
    yield prompt, filename

async def co_consume_prompts(producer_coroutine):
  client = s_init_openai()
  async for prompt, filename in producer_coroutine:
    s_download_image(s_generate_image(client, prompt), filename)

# Coroutine Coordination Function (Async Entry Point)
async def co_run_images(template_key, arguments_key):
  producer_coroutine = co_produce_prompts(template_key, arguments_key)
  await co_consume_prompts(producer_coroutine)

############################################################

def run_discord_bot():
  asyncio.run(bot.start(DISCORD_SECRET))

#async def a_callback():
#  asyncio.run(co_run_images("gothfembust", "sevenschools"))
#  return None

def run_flask():
  app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
  threading.Thread(target=run_discord_bot).start()
  run_flask()
