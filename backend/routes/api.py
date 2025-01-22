from fastapi import APIRouter, Request, HTTPException, status
from jose import jwt
from commands.images import generate_image
from commands.postgres import get_public_template, get_layer_template, get_user_from_database, make_new_user_for_database# It makes sense to create services modules that wrap these database functions in a more abstract manner
from services.auth import fetch_user_profile, verify_id_token
from utils.helpers import StateHelper

router = APIRouter()

# @router.get("auth/test")
# async def handle_test(request: Request, token: str = Depends(HTTPBearer)):
#   return status.HTTP_200_OK

@router.post("/auth/login")
async def handle_login(request: Request):
  state = StateHelper(request)

  # Get the JSON data from the POST
  request_data = await request.json()

  # Extract the idToken to perform RSA validation
  id_token = request_data.get("idToken")
  if not id_token:
    raise HTTPException(status_code=400, detail="ID Token is required.")

  # Extract verified subject
  payload = await verify_id_token(state, id_token)

  unique_identifier = payload.get("sub")
  if not unique_identifier:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

  # Extract the accessToken to perform Microsoft Graph API lookup
  access_token = request_data.get("accessToken")
  if not access_token:
    raise HTTPException(status_code=400, detail="Access Token is required.")

  # Get Microsoft Graph API user details
  ms_profile = await fetch_user_profile(access_token)

  # Report login processing
  await state.channel.send(f"Processing login for: {ms_profile["username"]}, {ms_profile["email"]}")

  ################################################################################
  # Look up user in DB, create new user if none found.
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

  request_data = await request.json()

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