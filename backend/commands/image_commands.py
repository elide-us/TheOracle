import asyncio, aiohttp, io, discord
from openai import OpenAIError
from typing import Dict
from datetime import datetime, timezone
from services.local_json import load_json
from services.blob_storage import get_container_client

###############################################################################
## Basic Helper Functions
###############################################################################

def generate_filename(identifier: str, extension: str = ".png") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{timestamp}_{identifier}{extension}"

class SafeDict(dict):
    def __missing__(self, key):
        return ''

###############################################################################
## Data Access Functions
###############################################################################

async def get_template(template_key: str) -> str:
    templates_data = await load_json("data_templates.json")
    if not templates_data:
        raise ValueError("Error loading data_templates.json")
    if template_key not in templates_data:
        raise ValueError(f"Key '{template_key}' not found in data_templates.json")
    return templates_data[template_key]

async def get_elements(selected_keys: Dict[str, str]) -> Dict[str, str]:
    elements = {}

    async def fetch_element(key: str, value: str):
        file_path = f"data/{key}.json"
        data = await load_json(file_path)
        
        if data is None:
            raise ValueError(f"Error loading '{file_path}': File does not exist or could not be read.")
        
        if not isinstance(data, dict):
            raise ValueError(f"Error parsing '{file_path}': Expected a JSON object at the top level.")
        
        if value not in data:
            raise ValueError(f"Key '{value}' not found in '{file_path}'.")
        
        element = data[value]
        description = element.get("private")
        
        if not isinstance(description, str):
            raise ValueError(f"Invalid data for key '{value}' in '{file_path}': Expected a string description.")
        
        elements[key] = description
    
    tasks = [
        fetch_element(key, value)
        for key, value in selected_keys.items()
    ]

    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        # You can choose to handle exceptions differently, e.g., continue on errors
        raise e

    return elements

###############################################################################
## Internal Processing Functions
###############################################################################

# Compile the final text
async def format_template(template: str, replacements: dict) -> str:
    return template.format_map(SafeDict(replacements))

# Gather the data and return the final text
async def format_prompt(template_key: str, selected_keys: dict, user_input: str) -> str:
    template = await get_template(template_key)
    elements = await get_elements(selected_keys)
    
    return await format_template(template, elements) + "*Main Subject Prompt*: " + user_input

# Send the image create request to OpenAI
async def post_request(client, prompt):
  try:
    completion = await client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      style="vivid",
      size="1792x1024",
      n=1
    )
  except OpenAIError as e:
      raise

  if not completion.data:
    raise ValueError("No image returned from OpenAI.")

  return completion.data[0].url

# Write buffer out to Discord channel
async def write_discord(buffer, bot, filename):
  buffer.seek(0)
  channel = bot.get_channel(bot.sys_channel)
  await channel.send(file=discord.File(fp=buffer, filename=filename))

# Write buffer out to CDN
async def write_cdn(buffer, filename):
  buffer.seek(0)
  container_client = await get_container_client()
  await container_client.upload_blob(data=buffer, name=filename, overwrite=True)

# Async Context Manager for buffer
class AsyncBufferWriter():
  def __init__(self, url):
    self.buffer = None
    self.url = url

  async def __aenter__(self):
    self.buffer = await self._fetch_buffer()
    return self.buffer
  
  async def _fetch_buffer(self):
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(self.url) as response:
          response.raise_for_status()
          return io.BytesIO(await response.read())
    except aiohttp.ClientError as e:
      raise ValueError(f"Failed to fetch buffer from {self.url}: {str(e)}")

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    if self.buffer:
      self.buffer.close()


async def process_image(image_url: str, template_key: str, bot) -> str:
  filename = generate_filename(template_key)

  async with AsyncBufferWriter(image_url) as buffer:
    await write_discord(buffer, bot, filename)
    await write_cdn(buffer, filename)

  azure_image_url = f"https://theoraclesa.blob.core.windows.net/theoraclegpt/{filename}"
  return azure_image_url

###############################################################################
## Public Functions
###############################################################################

async def generate_image(app, bot, template_key: str, selected_keys: dict, user_input: str):
  try:
    prompt_text = await format_prompt(template_key, selected_keys, user_input)
    generated_image_url = await post_request(app.state.openai_client, prompt_text)

    return await process_image(generated_image_url, template_key, bot)
  
  except Exception as e:
    channel = bot.get_channel(bot.sys_channel)
    await channel.send(f"Error generating image: {str(e)}")
    return None
