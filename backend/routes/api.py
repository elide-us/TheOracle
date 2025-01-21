from fastapi import APIRouter, Request, HTTPException, status
from jose import jwt
from commands.image_commands import generate_image
from commands.db_commands import get_public_template, get_layer_template, get_user_from_database, make_new_user_for_database# It makes sense to create services modules that wrap these database functions in a more abstract manner
from services.auth import fetch_user_profile, verify_id_token
from typing import Any


router = APIRouter()

# @router.get("auth/test")
# async def handle_test(request: Request, token: str = Depends(HTTPBearer)):
#   return status.HTTP_200_OK

class StateHelper:
  def __init__(self, request: Request):
    self.request = request
  #   self.__state = request.app.state
  # def __getattr__(self, name):
  #   getattr(self.__state, name)
  @property
  def app(self) -> Any:
    return self.request.app
  @property
  def bot(self) -> Any:
    return self.request.app.state.discord_bot
  @property
  def channel(self) -> Any:
    return self.bot.get_channel(self.bot.sys_channel)
  @property
  def pool(self) -> Any:
    return self.request.app.state.db_pool
  @property
  def ms_api_id(self) -> Any:
    return self.request.app.state.microsoft_client_id
  @property
  def jwt_secret(self) -> Any:
    return self.request.app.state.jwt_secret
  @property
  def jwt_algorithm(self) -> Any:
    return self.request.app.state.jwt_algorithm
  @property
  def ms_jwks(self):
    return self.request.app.state.jwks # impl lazy loader
  @property
  def storage(self):
    return self.request.app.state.container_client

@router.post("/auth/login")
async def handle_login(request: Request):
  state = StateHelper(request)

  ################################################################################
  ## Auth Phase 1: Extract Data
  ################################################################################

  # Get the JSON data from the POST
  request_data = await request.json()

  # Extract the idToken to perform RSA validation
  id_token = request_data.get("idToken")
  if not id_token:
    raise HTTPException(status_code=400, detail="ID Token is required.")

  # Extract the accessToken to perform Microsoft Graph API lookup
  access_token = request_data.get("accessToken")
  if not access_token:
    raise HTTPException(status_code=400, detail="Access Token is required.")

  ################################################################################
  ## Auth Phase 2: Validate and Get Details
  ################################################################################

  # Validate idToken
  auth_payload = await verify_id_token(state, id_token)

  # Extract verified subject
  unique_identifier = auth_payload.get("sub")
  if not unique_identifier:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

  # Get Microsoft Graph API user details
  ms_profile = await fetch_user_profile(access_token)
  await state.channel.send(f"Processing login for: {ms_profile["username"]}, {ms_profile["email"]}")

  ################################################################################
  ## Auth Phase 3: Lookup Internal User
  ################################################################################

  # Look up user in DB, create new user if none found
  user = await get_user_from_database(state, unique_identifier)
  if not user:
    user = await make_new_user_for_database(state, unique_identifier, ms_profile["email"], ms_profile["username"])
    await state.channel.send(f"Added user for {user["guid"]}: {user["username"]}, {user["email"]}")
  await state.channel.send(f"Found user for {user["guid"]}: {user["username"]}, {user["email"]}")

  ################################################################################
  ## Auth Phase 4: Return Internal Bearer Token
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