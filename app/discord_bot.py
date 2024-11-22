import os
import discord
from discord.ext import commands

DISCORD_SECRET = os.getenv('DISCORD_SECRET')
OPENAI_SECRET = os.getenv('OPENAI_SECRET')
LUMAAI_SECRET = os.getenv('LUMAAI_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')



intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

#@bot.command(name='ai')
#async def ai(ctx):
#    await ctx.send("Online.")

async def start_discord_bot():
    # Start the bot asynchronously
    await bot.start(DISCORD_SECRET)
