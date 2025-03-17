from discord.ext import commands
from atproto import client_utils, AtUri
from utils.helpers import ContextHelper
from commands.discord import handle_text_generate

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
      # max_tokens = 3800
      # tokenizer = context.tokenizer

      post_text = f"uwu {message}. Here are the most recent posts for context, respond briefly and appropriately: "
      # post_tokens = len(tokenizer.encode(post_text))
      
      posts = await client.app.bsky.feed.post.list(client.me.did, limit=2)
      for uri, post in posts.records.items():
        # post_tokens += len(tokenizer.encode(post.text))
        post_text += f"# {post.text} "

      await context.sys_channel.send("DEBUG: Sending handle text generate.")
      e = await handle_text_generate(ctx, post_text, "bsky")
      if e:
        await context.sys_channel.send(f"Exception: {e}")

    case _:
      await context.sys_channel.send("DEBUG: case _")
