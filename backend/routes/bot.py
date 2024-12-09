from commands.dispatcher import get_dispatcher, parse_and_dispatch

def setup_bot_commands(bot, bot_channel_id):
  @bot.command(name="hello")
  async def hello(ctx):
    await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot_channel_id)
    if channel:
      await channel.send("TheOracleGPT Online.")

  @bot.command(name="imagen")
  async def imagen(ctx, *args):
    command_str = " ".join(args)
    channel = ctx.channel
    dispatcher = await get_dispatcher()
    openai_client = ctx.bot.app.state.openai_client
    response = await parse_and_dispatch(command_str, channel, dispatcher, openai_client)
    if response:
      await ctx.send(response)

  @bot.command(name="chat")
  async def chat(ctx, *args):
    command_str = " ".join(args)
    channel = ctx.channel
    await channel.send("Responding to !chat command.")
    # Get dispatcher for chat commands
    # Get OpenAI client
    # Dispatch chat coroutine

  @bot.command(name="video")
  async def video_gen(ctx, *args):
    command_str = " ".join(args)
    channel = ctx.channel
    await channel.send("Responding to !video command.")
    # Get dispatcher for video commands
    # Get LumaAI client
    # Dispatch video coroutine

  @bot.command(name="tts")
  async def tts_gen(ctx, *args):
    command_str = " ".join(args)
    channel = ctx.channel
    await channel.send("Responding to !tts command.")
    # Get dispatcher for tts commands
    # Get OpenAI client
    # Dispatch tts coroutine

  @bot.command(name="image")
  async def image_gen(ctx, *args):
    command_str = " ".join(args)
    channel = ctx.channel
    await channel.send("Responding to !image command.")
    # Get dispatcher for image commands
    # Get OpenAI client
    # Dispatch image coroutine
