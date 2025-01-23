import datetime
from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from commands.images import generate_image
from commands.postgres import get_public_template, get_layer_template, get_database_user, make_database_user
from services.auth import process_login, make_bearer_token
from utils.helpers import StateHelper

router = APIRouter()

def decode_jwt(state: StateHelper, token: str):
  try:
    payload = jwt.decode(token, state.jwt_secret, algorithms=[state.jwt_algorithm])

    # Simple expiry validation, will obviously need to validate against the database backend...
    exp = payload.get("exp")
    if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"}
      )
    return payload
  except JWTError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token",
      headers={"WWW-Authenticate": "Bearer"}
    )

@router.get("/auth/test")
async def handle_test(request: Request, token: str = Depends(HTTPBearer())):
  state = StateHelper(request)

  auth_token = token.credentials
  user_payload = decode_jwt(state, auth_token)

  return {
    "message": "Token is valid",
    "user": user_payload,  # Return the decoded payload for demonstration purposes
  }

@router.post("/auth/login")
async def handle_login(request: Request):
  state = StateHelper(request)

  unique_identifier, ms_profile = await process_login(request)

  user = await get_database_user(state, unique_identifier)
  if not user:
    user = await make_database_user(state, unique_identifier, ms_profile["email"], ms_profile["username"])

  return {"bearerToken": make_bearer_token(state, str(user["guid"])), "email": user["email"], "username": user["username"], "profilePicture": ms_profile["profilePicture"]}

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