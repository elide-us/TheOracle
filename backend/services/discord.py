import discord
from discord.ext import commands
from conf.env import get_discord_token
from commands.tts_commands import handle_tts
#from commands.text_commands import handle_chat
#from services.local_json import load_json

async def init_discord_bot():
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    return commands.Bot(command_prefix='!', intents=intents)

def setup_bot_routes(bot):
  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot.sys_channel)
    if channel:
      await channel.send("TheOracleGPT Online.")

  @bot.command(name="tts")
  async def tts_gen(ctx, *args):
    command_str = " ".join(args)
    response = await handle_tts(ctx, command_str)
    if response:
      await ctx.send(response)

  # @bot.command(name="hello")
  # async def hello(ctx):
  #   await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  # @bot.command(name="assistants", help="Lists the assistants available for the !chat command.")
  # async def assistants(ctx, *args):
  #   data = await load_json("data_assistants.json")
  #   assistants_list = ", ".join(data.keys())
  #   await ctx.send(f"Available assistants: {assistants_list}")

  # @bot.command(name="chat", help="Format: !chat <assistant> <Your question here.> Each assistant is tuned to provide specific expertise.")
  # async def chat(ctx, *args):
  #   command_str = " ".join(args)
  #   response = await handle_chat(ctx, command_str)
  #   if response:
  #     await ctx.send(response)

  # @bot.command(name="video")
  # async def video_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   lumaai_client = ctx.bot.app.state.lumaai_client
  #   response = await handle_video(command_str, lumaai_client)
  #   if response:
  #     await ctx.send(response)
 
  # @bot.command(name="image")
  # async def image_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   openai_client = ctx.bot.app.state.openai_client
  #   response = await handle_image(command_str, openai_client)
  #   if response:
  #     await ctx.send(response)

async def start_discord_bot(bot):
    token = get_discord_token()
    await bot.start(token)
