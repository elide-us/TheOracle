import os
import logging
import asyncio
import threading
import discord
from discord.ext import commands
from flask import Flask #request, jsonify

class FlaskWrapper:
  def __init__(self):
    self.logger = logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    self._setup_logger()
    self.app = Flask(__name__)
    self._setup_routes()
    self.intents = discord.Intents.default()
    self.discord_token = os.getenv('DISCORD_SECRET')
    self.discord_channel = os.getenv('DISCORD_CHANNEL')
    self._setup_discord()
 
  async def imagen(self):
    self.logger.info("imagen()")
    bot = self.bot
    bot_token = self.discord_token
    bot_channel = int(self.discord_channel)

    @bot.event
    async def on_ready():
      channel = bot.get_channel(bot_channel)
      if channel:
        await channel.send("imagen Online.")

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

    await bot.start(bot_token)

  def run_discord_bot(self):
    self.logger.info("run_discord_bot()")
    asyncio.run(self.imagen(self))

  def run_flask_app(self):
    self.logger.info("run_flask_app()")
    self.app.run()

  def _setup_logger(self):
    self.logger = logging.getLogger(self)

  def _setup_discord(self):
    self.intents.messages = True
    self.intents.message_content = True
    self.bot = commands.Bot(command_prefix='!', intents=self.intents)

  def _setup_routes(self):
    @self.app.route('/')
    def index():
      return "Hello from FlaskWrapper!"

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

  def __call__(self, environ, start_response):
    return self.app.wsgi_app(environ, start_response)

  def run(self):
    # Start background task in a separate thread.
    threading.Thread(target=self.run_discord_bot, daemon=True).start()
    # Run Flask in the main thread.
    self.run_flask_app()

app = FlaskWrapper()
