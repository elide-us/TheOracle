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
  
  async def get_discord_channel_id(self):
    return get_discord_channel()

  def setup_routes(self):
    from routes.bot import setup_bot_routes
    setup_bot_routes(self.bot)

  @classmethod
  async def create(cls, app):
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    app.state.discord_bot = bot
    bot.app = app

    instance = cls(app, bot)
    instance.setup_routes()

    bot.sys_channel = instance.get_discord_channel_id()
    # bot.sys_channel = await instance.get_discord_channel_id("sys_channel")
    # bot.out_channel = await instance.get_discord_channel_id("out_channel")
    # bot.cmd_channel = await instance.get_discord_channel_id("cmd_channel")

    return instance
  
async def start_bot(self):
    token = get_discord_token()
    await self.bot.start(token)
