import io, asyncio
from openai import OpenAIError
from typing import Dict
from datetime import datetime, timezone
from commands.discord import write_buffer_to_discord
from commands.storage import write_buffer_to_blob
from commands.postgres import select_prompt_keys
from utils.helpers import StateHelper, AsyncBufferWriter, SafeDict, load_json

###############################################################################
## Basic Helper Functions
###############################################################################

def generate_filename(identifier: str, extension: str = ".png") -> str:
  timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
  return f"{timestamp}_{identifier}{extension}"

def generate_filename_url(filename: str):
  return f"https://theoraclesa.blob.core.windows.net/theoraclegpt/{filename}"

###############################################################################
## Data Access Functions
###############################################################################

async def get_template(template_key: str) -> str:
  templates_data = await load_json("data_templates.json")

  if template_key not in templates_data:
    raise ValueError(f"Key '{template_key}' not found in data.")
  return templates_data[template_key]

async def get_elements(state: StateHelper, selected_keys: Dict[str, str]) -> Dict[str, str]:
  await state.channel.send("Getting elements from local files")
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
    raise e

  return elements

###############################################################################
## Internal Processing Functions
###############################################################################

# Compile the final text
async def format_template(template: str, replacements: dict) -> str:
  return template.format_map(SafeDict(replacements))

# Gather the data and return the final text
async def format_prompt(state: StateHelper, template_key: str, selected_keys: dict, user_input: str) -> str:
  template = await get_template(template_key)
  elements = await get_elements(state, selected_keys)
  # elements = await select_prompt_keys(state, selected_keys)
  
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

# Handles downloading and storing the resultant image
async def process_image(image_url: str, template_key: str, state: StateHelper) -> str:
  filename = generate_filename(template_key)

  async with AsyncBufferWriter(image_url) as buffer:
    await write_buffer_to_discord(buffer, state, filename)
    await write_buffer_to_blob(buffer, state, filename)

  return generate_filename_url(filename)

###############################################################################
## Imagen API Functions
###############################################################################

async def generate_image(state: StateHelper, template_key: str, selected_keys: dict, user_input: str):
  try:
    prompt_text = await format_prompt(state, template_key, selected_keys, user_input)
    generated_image_url = await post_request(state.openai, prompt_text)

    return await process_image(generated_image_url, template_key, state)
  except Exception as e:
    await state.channel.send(f"Error generating image: {str(e)}")
    return None

###############################################################################
## TTS API Functions
###############################################################################

# Updated to use new StateHelper from_context
async def handle_tts(ctx, command_str):
  state = StateHelper.from_context(ctx)
  client = state.openai
  
  split = command_str.split(" ")
  prefix, voice = split[0], split[1]
  text = " ".join(split[2:])
  filename = f"{prefix}_{voice}_{text}.mp3"

  await state.channel.send(f"Starting TTS generation for text: {text}")

  try:
    buffer = io.BytesIO()
    async with client.audio.speech.with_streaming_response.create(
      model='tts-1',
      voice=voice,
      input=text
    ) as response:
      async for chunk in response.iter_bytes():
        buffer.write(chunk)  # Write chunks to the buffer
      await write_cdn(buffer, state, filename)
      await write_buffer_to_discord(buffer, state, filename)
  except Exception as e:
    await state.channel.send(f"Error communicating with OpenAI: {str(e)}")
    return
  