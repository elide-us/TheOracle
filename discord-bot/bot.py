import discord

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
  print("on_ready()")

bot.run(DISCORD_TOKEN)
