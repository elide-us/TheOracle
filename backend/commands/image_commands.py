import asyncio, aiohttp, io, discord
from openai import OpenAIError
from typing import Dict
from datetime import datetime, timezone
from services.local_json import load_json
from services.blob_storage import get_container_client

###############################################################################
# Basic Helper Functions
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
        
        description = data[value]
        
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

def generate_filename(identifier: str, extension: str = ".png") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{timestamp}_{identifier}{extension}"

class SafeDict(dict):
    def __missing__(self, key):
        return ''

async def format_template(template: str, replacements: dict) -> str:
    return template.format_map(SafeDict(replacements))

async def build_prompt(template_key: str, selected_keys: dict, user_input: str) -> str:
    template = await get_template(template_key)
    elements = await get_elements(selected_keys)
    
    return await format_template(template, elements) + "*Main Subject Prompt*: " + user_input

###############################################################################
# Image Generation Flow
###############################################################################

async def download_and_post_image(image_url: str, template_key: str, bot) -> str:
    print("download_and_post_image")
    channel = bot.get_channel(bot.sys_channel)
    container_client = await get_container_client()
    buffer = io.BytesIO()
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                buffer.write(await response.read())
            else:
                raise ValueError(f"Failed to download image (Status: {response.status}).")

    filename = generate_filename(template_key)

    buffer.seek(0)
    await channel.send(file=discord.File(fp=buffer, filename=filename))

    buffer.seek(0)
    await container_client.upload_blob(data=buffer, name=filename, overwrite=True)

    azure_image_url = f"https://theoraclesa.blob.core.windows.net/theoraclegpt/{filename}"
    return azure_image_url

async def generate_and_upload_image(app, bot, template_key: str, selected_keys: dict, user_input: str):
    openai_client = app.state.openai_client
    
    try:
        prompt_text = await build_prompt(template_key, selected_keys, user_input)
        print(f"Prompt: {prompt_text}")

        completion = await openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            style="vivid",
            size="1792x1024",
            n=1
        )

        # Check for errors in the response
        if hasattr(completion, 'error') and completion.error:
            error_message = completion.error.message if hasattr(completion.error, 'message') else 'An error occurred.'
            raise ValueError(f"OpenAI API error: {error_message}")

        # Validate the response data
        if not completion or not hasattr(completion, 'data') or len(completion.data) == 0:
            raise ValueError("No image returned from OpenAI.")

        generated_image_url = completion.data[0].url
        print(f"{generated_image_url}")

        blob_image_url = await download_and_post_image(generated_image_url, template_key, bot)

        return blob_image_url

    except OpenAIError as e:
        # Handle OpenAI API errors
        print(f"OpenAI API error: {e}")
        raise
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        raise

