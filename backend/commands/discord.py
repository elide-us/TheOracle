from utils.messaging import send_to_discord
from services.local_json import load_json

async def handle_text_generate(ctx, command_str):
  app = ctx.bot.app
  bot = ctx.bot
  channel = ctx.channel
  client = app.state.openai_client
  
  split = command_str.split(" ")
  key = split[0]
  prompt = " ".join(split[1:])

  json = await load_json("data_assistants.json")
  if not json:
    await channel.send("Error loading assistant data.")
    return

  assistant = json[key]
  if not assistant:
    await channel.send(f"Error loading assistant: {key} not found.")
    return

  channel.send(f"Sending prompt to OpenAI: {prompt}")
  try:
    completion = await client.chat.completions.create(
      model=assistant["model"],
      max_tokens=assistant["max_tokens"],
      messages=[
        {"role": "system", "content": assistant["role"]},
        {"role": "user", "content": prompt}
      ]
    )
    response_text = completion.choices[0].message.content
  except Exception as e:
    await channel.send(f"Error communicating with OpenAI: {str(e)}")
    return
  
  response_text = completion.choices[0].message.content
  await send_to_discord(channel, response_text)
