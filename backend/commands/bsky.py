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
      await ctx.channel.send(f"{post.uri}, {post.cid}, {profile.display_name}")
    case "list":
      posts = await client.app.bsky.feed.post.list(client.me.did, limit=2)
      for uri, post in posts.records.items():
        await ctx.channel.send(f"{uri}, {post.text}")
    case "uwu":
      # max_tokens = 3800
      # tokenizer = context.tokenizer

      post_text = ""
      # post_tokens = len(tokenizer.encode(post_text))
      
      posts = await client.app.bsky.feed.post.list(client.me.did, limit=5)
      for post in posts.records.items():
        # post_tokens += len(tokenizer.encode(post.text))
        post_text += f"# {post.text} "

      command_str = f"uwu {message}. Here are the most recent posts for context, respond briefly and appropriately: {post_text}."
      e = await handle_text_generate(ctx, command_str, "bsky")

    case _:
      return None
  return None
