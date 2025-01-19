from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt
from typing import Dict
from commands.image_commands import generate_image
from commands.db_commands import get_public_template, get_layer_template, get_user_from_database, make_new_user_for_database
import aiohttp, base64

router = APIRouter()

async def fetch_openid_config(app):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://login.microsoftonline.com/consumers/v2.0/.well-known/openid-configuration") as response:
      if response.status != 200:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Failed to fetch OpenID configuration.")
      openid_config = await response.json()
      app.state.jwks_url = openid_config["jwks_uri"]

async def fetch_jwks(app): 
  async with aiohttp.ClientSession() as session:
    async with session.get(app.state.jwks_url) as response:
      if response.status != 200:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Failed to fetch JWKS.")
      app.state.jwks = await response.json()

async def get_jwks(app):
  if not hasattr(app.state, "jwks") or not app.state.jwks:
    if not hasattr(app.state, "jwks_uri"):
      await fetch_openid_config(app)
    await fetch_jwks(app)
  return app.state.jwks

async def verify_id_token(app, id_token: str, client_id: str) -> Dict:
  jwks = await get_jwks(app)

  try:
    unverified_header = jwt.get_unverified_header(id_token)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid ID token.")

  rsa_key = next(
    (
      {
        "kty": key["kty"],
        "kid": key["kid"],
        "use": key["use"],
        "n": key["n"],
        "e": key["e"],
      }
      for key in jwks["keys"]
      if key["kid"] == unverified_header["kid"]
    ),
    None,
  )
  if not rsa_key:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header.")
  
  try:
    payload = jwt.decode(
      id_token,
      rsa_key,
      algorithms=["RS256"],
      audience=client_id,
      issuer="https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/v2.0"
    )
    return payload
  
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
  except jwt.JWTClaimsError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect claims. Please check the audience and issuer.")
  except Exception:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed.")

async def fetch_user_profile(access_token: str):
  async with aiohttp.ClientSession() as session:
    headers = {"Authorization": f"Bearer {access_token}"}

    async with session.get("https://graph.microsoft.com/v1.0/me", headers=headers) as response:
      if response.status != 200:
        error_message = await response.text()
        raise HTTPException(status_code=500, detail=f"Failed to fetch user profile. Status: {response.status}, Error: {error_message}")
      user = await response.json()
    
    # Fetch profile picture data
    profile_picture_bytes = None
    async with session.get("https://graph.microsoft.com/v1.0/me/photo/$value", headers=headers) as response:
      if response.status == 200:
        profile_picture_bytes = await response.read()
        profile_picture_base64 = base64.b64encode(profile_picture_bytes).decode("utf-8")

    # Return structured user data
    return {
      "email": user.get("mail") or user.get("userPrincipalName"),  # Handle fallback for email
      "username": user.get("displayName"),
      "profilePicture": profile_picture_base64
    }

@router.post("/auth/login")
async def handle_login(request: Request):
  app = request.app
  bot = app.state.discord_bot
  channel = bot.get_channel(bot.sys_channel)
  pool = app.state.db_pool
  await channel.send("Processing login...")

  data = await request.json()
  id_token = data.get("idToken")
  if not id_token:
    raise HTTPException(status_code=400, detail="ID Token is required.")

  access_token = data.get("accessToken")
  if not access_token:
    raise HTTPException(status_code=400, detail="Access Token is required.")

  client_id = app.state.microsoft_client_id
  payload = await verify_id_token(app, id_token, client_id)

  microsoft_id = payload.get("sub")
  if not microsoft_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

  user_profile = await fetch_user_profile(access_token)
  username = user_profile["username"]
  email = user_profile["email"]
  await channel.send(f"{username}, {email}")

  user = await get_user_from_database(app, pool, microsoft_id)
  if not user:
    user = await make_new_user_for_database(app, pool, microsoft_id, email, username)
    await channel.send(f"Added user for {username}")
  await channel.send(f"Found user for {username}")

  token_data = {"sub": microsoft_id}
  token = jwt.encode(token_data, app.state.jwt_secret, algorithm=app.state.jwt_algorithm)
  if not token:
    await channel.send("No token generated.")

  response_data = {"bearer_token": token, "email": email, "username": username, "profilePicture": user_profile["profilePicture"]}

  await channel.send(f"Returning response_data JSON")

  return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)

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