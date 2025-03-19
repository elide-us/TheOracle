from discord.ext import commands
from atproto import client_utils, AtUri
from utils.helpers import ContextHelper
from commands.discord import handle_text_generate
from commands.theoracle import talk_to_ceo, talk_to_cfo, talk_to_cto
from io import BytesIO
from fastapi import FastAPI

async def handle_bsky(ctx: commands.Context, command: str, message: str):
  client = ctx.bot.app.state.bsky_client
  profile = ctx.bot.app.state.bsky_profile

  context = ContextHelper(ctx)
  
  match command:
    case "post":
      text = client_utils.TextBuilder().text(message)
      post = await client.send_post(text)
      await client.like(post.uri, post.cid)
      await ctx.channel.send(f"{post.uri}, {profile.display_name}")
    case "list":
      posts = await client.app.bsky.feed.post.list(client.me.did, limit=2)
      for uri, post in posts.records.items():
        await ctx.channel.send(f"{post.text}")
    case "uwu":
      post_text = f"uwu {message}. Here are the most recent posts for context, respond briefly and appropriately: "
      posts = await client.app.bsky.feed.post.list(client.me.did, limit=5)
      for uri, post in posts.records.items():
        post_text += f"# {post.text} "
      await context.sys_channel.send("DEBUG: Sending handle text generate.")
      e = await handle_text_generate(ctx, post_text, "bsky")
      if e:
        await context.sys_channel.send(f"Exception: {e}")

    case "ceo":
      await talk_to_ceo(ctx, message)
    case "cto":
      await talk_to_cto(ctx, message)
    case "cfo":
      await talk_to_cfo(ctx, message)

    case _:
      await context.sys_channel.send("DEBUG: case _")

async def write_buffer_to_bsky(buffer: BytesIO, state: FastAPI.state, filename: str):
  
  return None
