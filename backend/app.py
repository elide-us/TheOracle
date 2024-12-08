import os, asyncio, discord
from discord.ext import commands
from openai import AsyncOpenAI
from lumaai import LumaAI
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from azure.storage.blob import BlobServiceClient

async def a_get_blob_connstr():
  connstr = os.getenv("AZURE_BLOB_CONNECTION_STRING")
  if not connstr:
    raise RuntimeError("error")
  else:
    return connstr

async def a_get_blob_container():
  container = os.getenv("AZURE_BLOB_CONTAINER_NAME")
  if not container:
    raise RuntimeError("error")
  else:
    return container

async def a_init_discord():
  intents = discord.Intents.default()
  intents.messages = True
  intents.message_content = True
  bot = commands.Bot(command_prefix='!', intents=intents)
  return bot

async def a_get_discord_token() -> str:
  secret = os.getenv('DISCORD_SECRET')
  if not secret:
    raise RuntimeError("ERROR: DISCORD_SECRET missing.")
  else:
    return secret

async def a_get_discord_channel() -> int:
  channel = int(os.getenv('DISCORD_CHANNEL'))
  if not channel:
    raise RuntimeError("ERROR: DISCORD_CHANNEL missing.")
  else:
    return channel

async def a_get_openai_token() -> str:
  secret = os.getenv('OPENAI_SECRET')
  if not secret:
    raise RuntimeError("ERROR: OPENAI_SECRET missing.")
  else:
    return secret

async def a_init_openai():
  token = await a_get_openai_token()
  return AsyncOpenAI(api_key=token)

async def a_get_lumaai_token() -> str:
  secret = os.getenv('LUMAAI_SECRET')
  if not secret:
    raise RuntimeError("ERROR: LUMAAI_SECRET missing.")
  else:
    return secret

async def a_init_lumaai():
  token = await a_get_lumaai_token()
  return LumaAI(auth_token=token)

async def send_to_discord(channel, text: str, max_message_size: int = 250, delay: float = 3.0):
  start = 0
  while start < len(text):
    # Find the end of the chunk
    end = min(start + max_message_size, len(text))
    # Check for a newline character within the chunk
    if '\n' in text[start:end]:
      end = text.rfind('\n', start, end) + 1  # Include the newline character
    else:
      # If no newline, just break at the max size
      end = min(start + max_message_size, len(text))
    # Extract the chunk and send it
    chunk = text[start:end].strip()
    if chunk:  # Only send non-empty chunks
      await channel.send(chunk)
      await asyncio.sleep(delay)
    # Move to the next chunk
    start = end

async def a_generate_text(prompt: str, client, channel) -> None:
  await channel.send("Sending text prompt to OpenAI.")
  completion = await client.chat.completions.create(
    model="chatgpt-4o-latest",
    max_completion_tokens=1000,
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
    ]
  )
  response_text = completion.choices[0].message.content
  await send_to_discord(channel, response_text)

async def a_handle_text_generate(args: str, channel: str, client):
  if len(args) < 1:
    await channel.send("Text generate requires a prompt.")
  prompt = " ".join(args)
  return await a_generate_text(prompt, client, channel)

async def a_get_dispatcher():
  return {
    "text": {
      "generate": lambda args, channel, client: a_handle_text_generate(args, channel, client)
    },
    "image": {
      # "generate": lambda args, channel: a_handle_image_generate(args, channel)
      # ,"list": lambda args: handle_image_list(args)
      # ,"delete": lambda args: handle_image_delete(args)
    },
    "audio": {
      # "generate": lambda args, channel: a_handle_audio_generate(args, channel)
      # ,"list": lambda args: handle_audio_list(args)
      # ,"delete": lambda args: handle_audio_delete(args)

    }
    ,"video": {
      # "generate": lambda args, channel: a_handle_video_generate(args, channel)
      # ,"append": lambda args: handle_video_append(args)
      # ,"list": lambda args: handle_video_list(args)
      # ,"delete": lambda args: handle_video_delete(args)
    }
  }

async def a_parse_and_dispatch(command: str, channel: str, dispatcher, openai_client):
  words = command.split()
  if len(words) < 2: # Basic input validation
    await channel.send("Invalid command format. Must include <result> <action>.")
  result, action = words[0], words[1]
  args = words[2:]
  if result not in dispatcher or action not in dispatcher[result]: # Dispatch map validation
    await channel.send(f"Unknown command: {result} {action}")
  response = await dispatcher[result][action](args, channel, openai_client)
  return response

# Think we'll probably make a class that does all the below stuff and provides accessors to get to the objects...

# Async context manager for FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
  bot = await a_init_discord()
  bot_token = await a_get_discord_token()
  bot_channel = await a_get_discord_channel()
  bot_dispatcher  = await a_get_dispatcher()
  openai_client = await a_init_openai()
  # lumaai_client = await a_init_lumaai()

  @bot.command(name="hello")
  async def hello(ctx):
    await ctx.send("Greetings from TheOracleGPT, an AI-powered Discord bot by Elideus!")

  @bot.event
  async def on_ready():
    channel = bot.get_channel(bot_channel)
    if channel:
      await channel.send("TheOracleGPT Online.")

  @bot.command(name="imagen")
  async def imagen(ctx, *args):
    command_str = " ".join(args)
    try:
      channel = ctx.channel
      response = await a_parse_and_dispatch(command_str, channel, bot_dispatcher, openai_client)
      if response:
        await ctx.send(response)
    except ValueError as e:
      await ctx.send(f"Error: {str(e)}")
    except Exception as e:
      await ctx.send(f"An unexpected error occurred: {str(e)}")

  loop = asyncio.get_event_loop()
  bot_task = loop.create_task(bot.start(bot_token))

  connstr = await a_get_blob_connstr
  container = await a_get_blob_container

  blob_service_client = BlobServiceClient.from_connection_string(connstr)
  container_client = blob_service_client.get_container_client(container)
  
  app.state.container_client = container_client

  try:
    yield  # Suspend context until FastAPI shuts down
  finally:
    channel = bot.get_channel(bot_channel)
    if channel:
      await channel.send("TheOracleGPT Shutting down.")
    await bot.close()
    bot_task.cancel()

# Create the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/files")
async def list_Files(request: Request):
  container_client = request.app.state.container_client
  blobs = []
  async for blob in container_client.list_blobs():
    blobs.append(blob.name)
  return {"files": blobs}

@app.delete("/api/files/{filename}")
async def delete_file(filename: str, request: Request):
    container_client = request.app.state.container_client
    await container_client.delete_blob(filename)
    return {"status": "deleted", "file": filename}

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # Always return index.html to support SPA routing
    return FileResponse("static/index.html")
