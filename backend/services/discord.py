import discord
from discord.ext import commands
from config.env import get_discord_token

async def init_discord_bot():
  intents = discord.Intents.default()
  intents.messages = True
  intents.message_content = True
  return commands.Bot(command_prefix='!', intents=intents)

async def start_discord_bot(bot):
  token = get_discord_token()
  await bot.start(token)
