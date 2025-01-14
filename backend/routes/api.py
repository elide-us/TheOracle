from fastapi import APIRouter, Request
import json
from commands.image_commands import generate_image
from commands.db_commands import get_public_template, get_layer_template

router = APIRouter()

@router.get("/files")
async def list_files(request: Request):
    container_client = request.app.state.container_client
    container_name = container_client.container_name
    base_url = f"https://theoraclesa.blob.core.windows.net/{container_name}/"  # Replace with your actual base URL
    blobs = []
    async for blob in container_client.list_blobs():
        blobs.append({
            "name": blob.name,
            "url": f"{base_url}{blob.name}"
        })
    return {"files": blobs}

# @router.delete("/files/{filename}")
# async def delete_file(filename: str, request: Request):
#   container_client = request.app.state.container_client
#   await container_client.delete_blob(filename)
#   return {"status": "deleted", "file": filename}

# @router.post("/files")
# async def upload_file(filename: str, request: Request):
#   container_client = request.app.state.container_client
#   await container_client.upload_blob(filename)
#   return {"status": "uploaded", "file": filename}

@router.post("/imagen")
async def image_generation(request: Request):
  incoming_data = await request.json()

  app = request.app
  bot = app.state.discord_bot

  template_key = incoming_data.get("template", "default")
  user_input = incoming_data.get("userinput", "")
  selected_keys = incoming_data.get("keys", {})

  try:
    azure_image_url = await generate_image(app, bot, template_key, selected_keys, user_input)
    return { "imageUrl": azure_image_url }
  except Exception as e:
    return {"error": str(e)}

@router.get("/imagen/{template_id}")
async def get_template(template_id: int, request: Request):
  match template_id:
    case 0:
      return await get_public_template(request.app.state.db_pool)
    case 1:
      return await get_layer_template(request.app.state.db_pool, 1)
    case 2:
      return await get_layer_template(request.app.state.db_pool, 2)
    case 3:
      return await get_layer_template(request.app.state.db_pool, 3)
    case 4:
      return await get_layer_template(request.app.state.db_pool, 4)
    case _:
      return {}

# @router.post("/lumagen")
# async def video_generation(request: Request):
#     incoming_data = await request.json()

#     app = request.app
#     bot = app.state.discord_bot

#     return None