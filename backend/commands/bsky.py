from discord.ext import commands
from atproto import client_utils

async def handle_bsky(ctx: commands.Context, command: str, message: str):
  client = ctx.bot.app.state.bsky_client
  profile = ctx.bot.app.state.bsky_profile
  
  match command:
    case "post":
      text = client_utils.TextBuilder().text(message)
      post = await client.send_post(text)
      await client.like(post.uri, post.cid)
      await ctx.channel.send(f"{post.uri}, {post.cid}, {profile.display_name}")
    case _:
      return None
    
  return None




