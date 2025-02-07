import discord
from discord.ext import commands
from commands.openai import handle_tts
from commands.discord import handle_text_generate, summarize
from utils.helpers import StateHelper, load_json
from services.env import get_discord_token
from commands.video_commands import generate_video

async def start_discord_bot(bot):
  token = get_discord_token()
  await bot.start(token)

async def init_discord_bot():
  intents = discord.Intents.default()
  intents.messages = True
  intents.guilds = True
  intents.message_content = True
  return commands.Bot(command_prefix='!', intents=intents)

def setup_bot_routes(bot: commands.Bot):
  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot.sys_channel)
    await channel.send("TheOracleGPT Online.")

  @bot.event
  async def on_guild_join(guild):
    channel = bot.get_channel(bot.sys_channel)
    if channel:
      await channel.send(f"Joined {guild.name} ({guild.id})")

  @bot.command(name="tts", help="!tts <prefix> <voice> <text to generate> Will convert text to speech for provided text.")
  async def command_tts(ctx, *args):
    state = StateHelper.from_context(ctx)
    command_str = " ".join(args)
    response = await handle_tts(state, command_str)
    if response:
      await state.channel.send(response)

  # @bot.command(name="hello", help="Provides a greeting message.")
  # async def command_hello(ctx):
  #   await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  @bot.command(name="summarize", help="!summarize <hours> Will collect message history for defined hours (default 1) and provide a summary.")
  async def command_summarize(ctx, hours: int = 1):
    text = await summarize(ctx, hours)

    command_str = f"summary Summarize the following conversations: {text}"
    e = await handle_text_generate(ctx, command_str, "user")
    if e:
      await ctx.send(f"Exception: {e}")

  @bot.command(name="assistants", help="Lists the assistants available for the !chat command.")
  async def command_assistants(ctx, *args):
    data = await load_json("data_assistants.json")
    assistants_list = ", ".join(data.keys())
    await ctx.send(f"Available assistants: {assistants_list}")

  @bot.command(name="chat", help="!chat <assistant> <your question here> Each assistant is tuned to provide specific expertise.")
  async def command_chat(ctx, *args):
    command_str = " ".join(args)
    response = await handle_text_generate(ctx, command_str, "channel")
    if response:
      await ctx.send(response)

  @bot.command(name="video")
  async def command_video(ctx, *args):
    frame0 = args[0]
    frame1 = args[1]
    prompt = " ".join(args[2:])

    await generate_video(ctx, frame0, frame1, prompt)
 
  # @bot.command(name="image")
  # async def image_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   openai_client = ctx.bot.app.state.openai_client
  #   response = await handle_image(command_str, openai_client)
  #   if response:
  #     await ctx.send(response)