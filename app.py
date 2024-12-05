#import os
#import asyncio
#import threading
#import discord
#from discord.ext import commands
#from flask import Flask #request, jsonify

# class FlaskWrapper:
#   def __init__(self):
#     self.app = Flask(__name__)
#     self._setup_routes()
#     self.intents = discord.Intents.default()
#     self.discord_token = os.getenv('DISCORD_SECRET')
#     self.discord_channel = os.getenv('DISCORD_CHANNEL')
#     self._setup_discord()
  # async def imagen(self):
  #   print("imagen()")
  #   bot_channel = int(self.discord_channel)
    # @self.bot.event
    # async def on_ready():
    #   print("on_ready()")
    #   channel = self.bot.get_channel(bot_channel)
    #   if channel:
    #     await channel.send("imagen Online.")
    #@bot.command(name="imagen")
    #async def imagen(ctx, *args):
    #  command_str = " ".join(args)
    #  try:
    #    channel = ctx.channel
    #    response = await a_parse_and_dispatch(command_str, channel)
    #    if response:
    #      await ctx.send(response)
    #  except ValueError as e:
    #    await ctx.send(f"Error: {str(e)}")
    #  except Exception as e:
    #    await ctx.send(f"An unexpected error occurred: {str(e)}")
    # await self.bot.start(self.discord_token)
  # def run_discord_bot(self):
  #   print("run_discord_bot()")
  #   asyncio.run(self.imagen(self))
  # def run_flask_app(self):
  #   print("run_flask_app()")
  #   self.app.run()
  # def _setup_discord(self):
  #   print("_setup_discord()")
  #   self.intents.messages = True
  #   self.intents.message_content = True
  #   self.bot = commands.Bot(command_prefix='!', intents=self.intents)
  # def _setup_routes(self):
  #   print("_setup_routes()")
  #   @self.app.route('/')
  #   def index():
  #     return "Hello from FlaskWrapper!"
    #@self.app.route('/discord', methods=['GET', 'POST'])
    #def discord():
    #  if request.method == 'POST':
    #     data = request.get_json()
    #     if data and 'content' in data:
    #       return jsonify({"content":data['content']})
    #     else:
    #       return jsonify({"error":"Missing 'content' in payload"}), 400
    #  else:
    #    return "Hello World!"
  # def __call__(self, environ, start_response):
  #   return self.app.wsgi_app(environ, start_response)
  # def run(self):
  #   print("Run Discord bot")
  #   threading.Thread(target=self.run_discord_bot, daemon=True).start()
  #   print("Run Flask app")
  #   self.run_flask_app()

#app = FlaskWrapper()

#import os
#import asyncio
#import discord
#from discord.ext import commands
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Discord bot setup
#async def _setup_discord():
  # intents = discord.Intents.default()
  # intents.messages = True
  # intents.message_content = True

  # token = os.getenv('DISCORD_SECRET')

  # return commands.Bot(command_prefix="!", intents=intents), token

# Async context manager for FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
  # bot, token = await _setup_discord()

  # @bot.event
  # async def on_ready():
  #   print(f"Bot logged in as {bot.user}")

  # @bot.command()
  # async def hello(ctx):
  #   await ctx.send("Hello from Discord Bot!")

  # # Startup: Run the bot
  # loop = asyncio.get_event_loop()
  # bot_task = loop.create_task(bot.start(token))
  # print("Discord bot started")

  # try:
  #   yield  # Suspend context until FastAPI shuts down
  # finally:
  #   # Shutdown: Stop the bot
  #   await bot.close()
  #   bot_task.cancel()
  #   print("Discord bot stopped")
  
  yield

# Create the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running with a Discord bot!"}
