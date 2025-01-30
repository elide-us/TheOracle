import io, discord
from discord.ext import commands
from fastapi import FastAPI

async def handle_tts(ctx: commands.Context, command_str):
  app: FastAPI = ctx.bot.app

  client = app.state.openai_client
  container = app.state.theoraclesa_client
  
  split = command_str.split(" ")

  session, voice = split[0], split[1]
  text = " ".join(split[2:])

  await ctx.send(f"Starting TTS generation for text: {text}")

  blob_name = f"{session}_{voice}_{text}.mp3"

  try:
    buffer = io.BytesIO()
    await ctx.send("calling api")
    async with client.audio.speech.with_streaming_response.create(
      model='tts-1',
      voice=voice,
      input=text
    ) as response:
      async for chunk in response.iter_bytes():
        buffer.write(chunk)  # Write chunks to the buffer
      
      buffer.seek(0)  # Reset buffer position to the start

      # Upload the buffer to Azure Blob Storage
      await container.upload_blob(data=buffer, name=blob_name, overwrite=True)

      # Send the file to Discord
      buffer.seek(0)  # Reset buffer position again
      
      await ctx.send(file=discord.File(fp=buffer, filename=blob_name))      
  except Exception as e:
    await ctx.send(f"Error communicating with OpenAI: {str(e)}")
    return
  