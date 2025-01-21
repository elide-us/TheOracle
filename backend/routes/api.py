from fastapi import APIRouter, Request, HTTPException, status
from jose import jwt
from commands.image_commands import generate_image
from commands.db_commands import get_public_template, get_layer_template, get_user_from_database, make_new_user_for_database# It makes sense to create services modules that wrap these database functions in a more abstract manner
from services.auth import fetch_user_profile, verify_id_token, get_subject
from utils.helpers import StateHelper, TokenHelper

router = APIRouter()

# @router.get("auth/test")
# async def handle_test(request: Request, token: str = Depends(HTTPBearer)):
#   return status.HTTP_200_OK

@router.post("/auth/login")
async def handle_login(request: Request):
  state = StateHelper(request)
  tokens = TokenHelper(request)

  # Extract verified subject
  unique_identifier = await get_subject(await verify_id_token(state, tokens.id_token))

  # Get Microsoft Graph API user details
  ms_profile = await fetch_user_profile(tokens.access_token)
  await state.channel.send(f"Processing login for: {ms_profile["username"]}, {ms_profile["email"]}")

  ################################################################################
  ## This section will change with additional auth improvements
  ################################################################################

  # Look up user in DB, create new user if none found
  user = await get_user_from_database(state, unique_identifier)
  if not user:
    user = await make_new_user_for_database(state, unique_identifier, ms_profile["email"], ms_profile["username"])
    await state.channel.send(f"Added user for {user["guid"]}: {user["username"]}, {user["email"]}")
  await state.channel.send(f"Found user for {user["guid"]}: {user["username"]}, {user["email"]}")

  ################################################################################

  # Encode a token for the subject using their Unique Identifier
  token_data = {"sub": unique_identifier}
  token = jwt.encode(token_data, state.jwt_secret, algorithm=state.jwt_algorithm)
  return {"bearer_token": token, "email": ms_profile["email"], "username": ms_profile["username"], "profilePicture": ms_profile["profilePicture"]}

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
  state = StateHelper(request)

  request_data = await request.json()

  app = request.app
  bot = app.state.discord_bot

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