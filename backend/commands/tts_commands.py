import io, discord

async def handle_tts(ctx, command_str):
  app = ctx.bot.app
  bot = ctx.bot
  channel = ctx.channel
  client = app.state.openai_client
  container = app.state.container_client
  
  split = command_str.split(" ")

  session, voice = split[0], split[1]
  text = " ".join(split[2:])

  await channel.send(f"Starting TTS generation for text: {text}")

  blob_name = f"{session}_{voice}_{text}.mp3"

  try:
    buffer = io.BytesIO()
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
      
      await channel.send(file=discord.File(fp=buffer, filename=blob_name))      
  except Exception as e:
    await channel.send(f"Error communicating with OpenAI: {str(e)}")
    return
  