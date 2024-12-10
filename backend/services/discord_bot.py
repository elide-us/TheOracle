import discord
from discord.ext import commands
from config import get_discord_token, get_discord_channel

# async def init_discord_bot():
#   intents = discord.Intents.default()
#   intents.messages = True
#   intents.message_content = True
#   return commands.Bot(command_prefix='!', intents=intents)

# async def start_discord_bot(bot):
#   token = get_discord_token()
#   await bot.start(token)

# async def get_discord_channel_id(channel: str = None) -> int:
#   return get_discord_channel()

class DiscordBot:
  def __init__(self, app, bot):
    self.app = app
    self.bot = bot

  def get_intents():
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    return intents  
  
  def setup_routes(self):
    from routes.bot import setup_bot_routes
    setup_bot_routes(self.bot)

  @classmethod
  async def create(cls, app):
    intents = DiscordBot.get_intents()
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.sys_channel = await instance.get_discord_channel_id()
    # bot.sys_channel = await instance.get_discord_channel_id("sys_channel")
    # bot.out_channel = await instance.get_discord_channel_id("out_channel")
    # bot.cmd_channel = await instance.get_discord_channel_id("cmd_channel")
    app.state.discord_bot = bot
    bot.app = app

    instance = cls(app, bot)
    instance.setup_routes()

    return instance
  
  async def start_bot(self):
    token = get_discord_token()
    await self.bot.start(token)

  async def get_discord_channel_id(self):
    return get_discord_channel()
  

