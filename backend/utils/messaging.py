import asyncio
from discord.ext import commands
from atproto import client_utils
from utils.helpers import ContextHelper

# A helper function that chunks and sends text to Discord to avoid flooding the gateway
async def send_to_discord(channel, text: str, max_message_size: int = 1998, delay: float = 1.0):
  for block in text.split("\n"):
    if not block.strip() or block.strip() == "---":
      continue  # Skip empty lines and lines containing only ----
    
    start = 0
    while start < len(block):
      # Find the end of the current chunk without breaking words
      end = min(start + max_message_size, len(block))
      if end < len(block) and block[end] != ' ':
        end = block.rfind(' ', start, end)  # Adjust to the last space
        if end == -1:  # If no spaces are found, force cut at max length
          end = start + max_message_size
      
      chunk = block[start:end].strip()
      if chunk:
        await channel.send(chunk)
        await asyncio.sleep(delay)
      
      start = end

async def send_to_discord_user(user, text: str, max_message_size: int = 1998, delay: float = 1.0):
  for block in text.split("\n"):
    if not block.strip() or block.strip() == "---":
      continue  # Skip empty lines and lines containing only ----
    
    start = 0
    while start < len(block):
      # Find the end of the current chunk without breaking words
      end = min(start + max_message_size, len(block))
      if end < len(block) and block[end] != ' ':
        end = block.rfind(' ', start, end)  # Adjust to the last space
        if end == -1:  # If no spaces are found, force cut at max length
          end = start + max_message_size
      
      chunk = block[start:end].strip()
      if chunk:
        await user.send(chunk)
        await asyncio.sleep(delay)
      
      start = end

async def send_to_bsky(ctx: commands.Context, message: str, max_message_size: int = 300, delay: float = 5.0):
  client = ctx.bot.app.state.bsky_client

  context = ContextHelper(ctx)
  await context.sys_channel.send("DEBUG: Send to bsky")

  for block in message.split("\n"):
    if not block.strip() or block.strip() == "---":
      continue  # Skip empty lines and lines containing only ----
    
    start = 0
    while start < len(block):
      # Find the end of the current chunk without breaking words
      end = min(start + max_message_size, len(block))
      if end < len(block) and block[end] != ' ':
        end = block.rfind(' ', start, end)  # Adjust to the last space
        if end == -1:  # If no spaces are found, force cut at max length
          end = start + max_message_size
      
      chunk = block[start:end].strip()
      if chunk:
        text = client_utils.TextBuilder().text(chunk)
        await client.send_post(text)
        await asyncio.sleep(delay)

  # client = ctx.bot.app.state.bsky_client
  # text = client_utils.TextBuilder().text(message)
  # await client.send_post(text)







