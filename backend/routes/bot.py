import io
import discord
from discord.ext import commands
from commands.discord import handle_text_generate, summarize, handle_command_assistants
from commands.lumaai import generate_video
from commands.openai import handle_tts
from commands.bsky import handle_bsky
from utils.messaging import send_to_bsky

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
    response = await handle_tts(ctx, *args)
    await ctx.send(response)

  @bot.command(name="uwu", help="!uwu will provide colorful context.")
  async def command_uwu(ctx, *args):
    text = await summarize(ctx, *args)

    command_str = f"uwu Provide contextual support, enthusiasm, and color for the recent conversations: {text}"
    e = await handle_text_generate(ctx, command_str, "channel")
    if e:
      await ctx.send(f"Exceptiopn: {e}")

  @bot.command(name="summarize", help="!summarize <hours> Will collect message history for defined hours (default 1) and provide a summary.")
  async def command_summarize(ctx, *args):
    text = await summarize(ctx, *args)

    command_str = f"summary Summarize the following conversations: {text}"
    e = await handle_text_generate(ctx, command_str, "user")
    if e:
      await ctx.send(f"Exception: {e}")

  @bot.command(name="assistants", help="Lists the assistants available for the !chat command.")
  async def command_assistants(ctx, *args):
    response = await handle_command_assistants(ctx, *args)
    await ctx.send(f"Available assistants: {response}")

  @bot.command(name="chat", help="!chat <assistant> <your question here> Each assistant is tuned to provide specific expertise.")
  async def command_chat(ctx, *args):
    command_str = " ".join(args)
    response = await handle_text_generate(ctx, command_str, "channel")
    if response:
      await send_to_bsky(ctx, response)
      await ctx.send(response)

  @bot.command(name="video")
  async def command_video(ctx, *args):
    frame0 = args[0]
    frame1 = args[1]
    prompt = " ".join(args[2:])
    await generate_video(ctx, frame0, frame1, prompt)
 
  # @bot.command(name="hello", help="Provides a greeting message.")
  # async def command_hello(ctx):
  #   await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  # @bot.command(name="image")
  # async def image_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   openai_client = ctx.bot.app.state.openai_client
  #   response = await handle_image(command_str, openai_client)
  #   if response:
  #     await ctx.send(response)

  @bot.command(name="bsky")
  async def command_bsky(ctx, *args):
    command = args[0]
    message = " ".join(args[1:])
    await handle_bsky(ctx, command, message)

  @bot.command(name="movemsg", help="!movemsg <channel name> Moves all messages in this channel to the specified channel if it exists.")
  async def command_movemsg(ctx, *args):
    if not args:
      await ctx.send("Please specify a target channel.")
      return

    target_name = args[0]
    target = discord.utils.get(ctx.guild.text_channels, name=target_name)
    if not target:
      await ctx.send(f"Channel '{target_name}' not found.")
      return

    moved = 0
    async for msg in ctx.channel.history(limit=None, oldest_first=True):
      if msg.id == ctx.message.id:
        continue
      files = []
      for attachment in msg.attachments:
        fp = await attachment.read()
        files.append(discord.File(io.BytesIO(fp), filename=attachment.filename))
      content = f"{msg.author.display_name}: {msg.content}" if msg.content else f"{msg.author.display_name}:"
      await target.send(content=content, files=files or None)
      await msg.delete()
      moved += 1

    await target.send(f"Moved {moved} messages from #{ctx.channel.name}.")
    await ctx.message.delete()
