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
  client = app.state.openai_client
  
  # Extract the first argument, this is the assistant and template that we're going to use for this prompt
  split = command_str.split(" ")
  key = split[0]
  prompt = split[1:]

  # Open the data_assistants.json file and load it
  json = await load_json("data_assistants.json")

  assistant = json[key] # This is a dict for use in the template.format call
  assistant.prompt = " ".join(prompt) # This is the prompt that the assistant will respond to

  # Open the data_templates.json file and load it
  template_data = await load_json("data_templates.json")
  template = template_data["chatresponse"]

  # Construct the client.chat.completions.create() call
  prompt = template.format(**assistant)

  completion = await client.chat.completions.create(prompt)
  response_text = completion.choices[0].message.content
  await send_to_discord(bot.sys_channel, response_text)
