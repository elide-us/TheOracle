import aiofiles, aiohttp
import discord
from datetime import datetime, timezone
from imagen_base import OPENAI, DATA_TEMPLATES, DATA_PALETTES

async def a_generate_text(prompt: str) -> str:
  """
  Generates text using OpenAI ChatGPT.
  """
  print("Sending text prompt to OpenAI.")
  client = await OPENAI.get()
  #client = AsyncOpenAI()
  completion = await client.chat.completions.create(
    model="chatgpt-4o-latest",
    max_completion_tokens=250,
    messages=[
      {"role":"system","content":"You are a helpful assistant."},
      {"role":"user","content":prompt}
    ]
  )
  return completion.choices[0].message.content

async def a_generate_audio(session, voice, text, channel):
  client = await OPENAI.get()
  file_path = f"{session}_{voice}_{text}.mp3"
  async with client.audio.speech.with_streaming_response.create(
    model='tts-1',
    voice=voice,
    input=text,
  ) as response:
    async with aiofiles.open(file_path, "wb") as file:
      async for chunk in response.iter_bytes():
        await file.write(chunk)
    print(f"Output: {file_path}")
  await channel.send(file=discord.File(file_path))

# Keys: gothfembust, benoit
async def a_get_template(key: str) -> str:
  """
  Loads an image template from data_templates.json.
  """
  print("Getting prompt template.")
  template_data = await DATA_TEMPLATES.get()
  print(f"Looking for key: '{key}'")
  print(f"Available keys: {list(template_data.keys())}")
  if key not in template_data:
    raise ValueError(f"Key '{key}' not found in JSON file.")
  return template_data[key]

async def a_get_palette(key: str) -> str:
  """
  Loads a palette argument from data_palettes.json
  """
  print("Getting palette argument.")
  palette_data = await DATA_PALETTES.get()
  print(f"Looking for key: '{key}'")
  print(f"Available keys: {list(palette_data.keys())}")
  if key not in palette_data:
    raise ValueError(f"Key '{key}' not found in JSON file.")
  return palette_data[key]

async def a_format_template(template: str, arguments: dict) -> str:
  """
  Replaces terms in template with values from matching keys in the dictionary
  """
  return template.format(**arguments)

async def a_generate_filename(identifier: str) -> str:
  timestamp = datetime.now(timezone.utc).strftime("%Y%M%d%H%M%S")
  filename = f"{timestamp}_{identifier}"
  print(f"Generated filename: {filename}.")
  return filename

async def a_generate_image(prompt: str) -> str:
  """
  Generates images using OpenAI DALL-E-3
  """
  print("Sending image prompt to DALL-E-3")
  client = await OPENAI.get()
  completion = await client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",
    quality="hd", # "standard"
    n=1
  )
  return completion.data[0].url

async def a_download_image(image_url, filename, channel):
  """
  Downloads an image from the given URL and posts it to the specified Discord channel.
  """
  print(f"Downloading: {filename}.png")
  async with aiohttp.ClientSession() as session:
    async with session.get(image_url) as response:
      if response.status == 200:
        file_path = f"{filename}.png"
        async with aiofiles.open(file_path, "wb") as file:
          await file.write(await response.read())
        print(f"{file_path} downloaded successfully.")
        if channel:
          await channel.send(file=discord.File(file_path))
          print(f"Image {file_path} posted to Discord channel.")
      else:
        print(f"Failed to download image. Status code: {response.status}")

async def a_make_dict(palette: str) -> dict:
  return {"palette":palette}

## I am aware this implementation is needlessly complicated with the co-routine, this was originally designed to work in batch
async def co_produce_prompt(template_key, palette_key, channel):
  """
  Takes the provided arguments, parses them and produces a prompt.
  """
  identifier = f"{template_key}_{palette_key}"
  print(f"Generating prompt: {identifier}")
  template = await a_get_template(template_key)
  palette = await a_get_palette(palette_key)
  palette_dict = await a_make_dict(palette)
  prompt = await a_format_template(template, palette_dict)
  #if not isinstance(arguments, dict):
    #raise ValueError("Arguments must be a dictionary for creating identifier.")
  #if len(arguments) < 2:
    #raise ValueError("Insufficient arguments to create identifier.")
  filename = await a_generate_filename(identifier)
  yield prompt, filename, channel

async def co_consume_prompt(producer_coroutine):
  """
  Consumer of produced prompts, sends generation requests to OpenAI and downloads the results.
  """
  print("Consuming prompt.")
  async for prompt, filename, channel in producer_coroutine:
    image_url = await a_generate_image(prompt)
    await a_download_image(image_url, filename, channel)

async def co_run_images(template_key, palette_key, channel):
  """
  Entry point for the co-routine that generates images from template prompts
  """
  producer_coroutine = co_produce_prompt(template_key, palette_key, channel)
  await co_consume_prompt(producer_coroutine)

################################################################################

def simple_parser(input_string):
  key_value_pairs = input_string.split(", ")
  result = {}
  for pair in key_value_pairs:
    key, value = map(str.strip, pair.split(":", 1))
    result[key] = value
  return result
