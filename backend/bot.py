import os
import discord
from discord.ext import commands

DISCORD_SECRET = os.getenv('DISCORD_SECRET')

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print("on_ready()")

@bot.command(name="ai")
async def ai(ctx):
  await ctx.send("Online.")

bot.run(DISCORD_SECRET)