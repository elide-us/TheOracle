import asyncio
from imagen_base import DISCORD, DISCORD_CHANNEL, DISCORD_TOKEN
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Async context manager for FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await DISCORD.get()
  bot_token = await DISCORD_TOKEN.get()
  bot_channel = await DISCORD_CHANNEL.get()

  @bot.command(name="hello")
  async def hello(ctx):
    await ctx.send("Hello from Discord Bot!")

  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot_channel)
    if channel:
      await channel.send("imagen Online.")

  # @bot.command(name="imagen")
  # async def imagen(ctx, *args):
  #   command_str = " ".join(args)
  #   try:
  #     channel = ctx.channel
  #     response = await a_parse_and_dispatch(command_str, channel)
  #     if response:
  #       await ctx.send(response)
  #   except ValueError as e:
  #     await ctx.send(f"Error: {str(e)}")
  #   except Exception as e:
  #     await ctx.send(f"An unexpected error occurred: {str(e)}")

  loop = asyncio.get_event_loop()
  bot_task = loop.create_task(bot.start(bot_token))

  try:
    yield  # Suspend context until FastAPI shuts down
  finally:
    await bot.close()
    bot_task.cancel()

# Create the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running with a Discord bot!"}

