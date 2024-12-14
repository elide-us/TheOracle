from utils.messaging import send_to_discord
from services.local_json import load_json

async def generate_text(prompt: str, client, channel) -> None:
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

async def handle_text_generate(args: str, channel, client):
  if len(args) < 1:
    await channel.send("Text generate requires a prompt.")
    return
  prompt = " ".join(args)
  return await generate_text(prompt, client, channel)

async def handle_chat(ctx, command_str):
  app = ctx.bot.app
  bot = ctx.bot
  channel = ctx.channel
  client = app.state.openai_client
  
  split = command_str.split(" ")
  key = split[0]
  prompt = split[1:]

  json = await load_json("data_assistants.json")
  if not json:
    await channel.send("Error loading assistant data.")
    return

  assistant = json[key]
  if not assistant:
    await channel.send(f"Error loading assistant: {key} not found.")
    return

  assistant.prompt = " ".join(prompt)

  # Open the data_templates.json file and load it
  template_data = await load_json("data_templates.json")
  if not template_data:
    await channel.send("Error loading template data.")
    return

  template = template_data["chatresponse"]
  if not template:
    await channel.send("Error loading template: chatresponse not found.")
    return

  prompt = template.format(**assistant)

  completion = await client.chat.completions.create(prompt)
  response_text = completion.choices[0].message.content
  await send_to_discord(bot.sys_channel, response_text)
