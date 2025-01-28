from fastapi import APIRouter, Request, Depends
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from commands.images import generate_image
from commands.postgres import get_public_template, get_layer_template, get_database_user, make_database_user, get_public_routes, get_secure_routes
from services.auth import process_login, make_bearer_token, decode_jwt
from utils.helpers import StateHelper

router = APIRouter()

@router.get("/routes")
async def get_routes(request: Request, token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())):
  state = StateHelper(request)
  await state.channel.send("routes")
  
  if token:
    await state.channel.send("with token")
    decoded_token = await decode_jwt(state, token.credentials)
    if not decoded_token:
      return {"error": "Invalid token"}
    
    user_guid = decoded_token.get("guid")
    if not user_guid:
      return {"error": "User GUID not found in token"}
    await state.channel.send("with guid")

    secure_routes = await get_secure_routes(state, user_guid)
    if secure_routes:
      await state.channel.send("with secure")
      return secure_routes
    
    await state.channel.send("without secure")
    return {"routes": [{'/', 'Home', 'home'}]}
  else:
    public_routes = await get_public_routes(state)
    await state.channel.send("with public")
    return public_routes

@router.post("/auth/login")
async def handle_login(request: Request):
  state = StateHelper(request)

  unique_identifier, ms_profile = await process_login(request)

  user = await get_database_user(state, unique_identifier)
  if not user:
    user = await make_database_user(state, unique_identifier, ms_profile["email"], ms_profile["username"])

  return {"bearerToken": make_bearer_token(state, str(user["guid"])), "email": user["email"], "username": user["username"], "profilePicture": ms_profile["profilePicture"], "credits": user["credits"]}

@router.get("/files")
async def list_files(request: Request):
  state = StateHelper(request)

  base_url = f"https://theoraclesa.blob.core.windows.net/{state.storage.container_name}/"  # Replace with your actual base URL
  blobs = []
  async for blob in state.storage.list_blobs():
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
  state = StateHelper(request)
  await state.channel.send("image_generation")
  request_data = await request.json()
  if not request_data:
    await state.channel.send("no request_data")
    
  template_key = request_data.get("template", "default")
  user_input = request_data.get("userinput", "")
  selected_keys = request_data.get("keys", {})

  try:
    azure_image_url = await generate_image(state, template_key, selected_keys, user_input)
    return { "imageUrl": azure_image_url }
  except Exception as e:
    return {"error": str(e)}

@router.get("/imagen/{template_id}")
async def get_template(template_id: int, request: Request):
  state = StateHelper(request)

  match template_id:
    case 0:
      return await get_public_template(state.pool)
    case 1:
      return await get_layer_template(state.pool, 1)
    case 2:
      return await get_layer_template(state.pool, 2)
    case 3:
      return await get_layer_template(state.pool, 3)
    case 4:
      return await get_layer_template(state.pool, 4)
    case _:
      return {}

# @router.post("/lumagen")
# async def video_generation(request: Request):
#     incoming_data = await request.json()

#     app = request.app
#     bot = app.state.discord_bot

#     return None