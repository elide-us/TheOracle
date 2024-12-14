from commands.text_commands import handle_chat

def setup_bot_routes(bot):
  @bot.command(name="hello")
  async def hello(ctx):
    await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot.sys_channel)
    if channel:
      await channel.send("TheOracleGPT Online.")

  # @bot.command(name="imagen")
  # async def imagen(ctx, *args):
  #   command_str = " ".join(args)
  #   channel = ctx.channel
  #   dispatcher = await get_dispatcher()
  #   openai_client = ctx.bot.app.state.openai_client
  #   response = await parse_and_dispatch(command_str, channel, dispatcher, openai_client)
  #   if response:
  #     await ctx.send(response)

  @bot.command(name="chat")
  async def chat(ctx, *args):
    command_str = " ".join(args)
    response = await handle_chat(ctx, command_str)
    if response:
      await ctx.send(response)

  # @bot.command(name="video")
  # async def video_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   lumaai_client = ctx.bot.app.state.lumaai_client
  #   response = await handle_video(command_str, lumaai_client)
  #   if response:
  #     await ctx.send(response)

  # @bot.command(name="tts")
  # async def tts_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   openai_client = ctx.bot.app.state.openai_client
  #   response = await handle_tts(command_str, openai_client)
  #   if response:
  #     await ctx.send(response)

  # @bot.command(name="image")
  # async def image_gen(ctx, *args):
  #   command_str = " ".join(args)
  #   openai_client = ctx.bot.app.state.openai_client
  #   response = await handle_image(command_str, openai_client)
  #   if response:
  #     await ctx.send(response)
