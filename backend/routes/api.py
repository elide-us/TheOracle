from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt
from typing import Dict
from commands.image_commands import generate_image
from commands.db_commands import get_public_template, get_layer_template, get_user_from_database
import aiohttp

router = APIRouter()

async def fetch_openid_config(app):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://login.microsoftonline.com/consumer/v2.0/.well-known/openid-configuration") as response:
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
  bot = app.state.discord_bot
  channel = bot.get_channel(bot.sys_channel)
  
  jwks = await get_jwks(app)

  await channel.send(f"ID Token: {id_token}")
  unverified_header = jwt.get_unverified_header(id_token)
  await channel.send(f"Unverified Header: {unverified_header}")


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
    await channel.send("DEBUG: Invalid token header.")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header.")
  
  try:
    await channel.send("DEBUG: Attempting jwt.decode()")
    payload = jwt.decode(
      id_token,
      rsa_key,
      algorithms=["RS256"],
      audience=client_id,
      issuer="https://login.microsoftonline.com/consumer/v2.0"
    )
    return payload
  
  except jwt.ExpiredSignatureError:
    await channel.send("DEBUG: Token has expired.")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
  except jwt.JWTClaimsError:
    await channel.send("DEBUG: Incorrect claims.")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect claims. Please check the audience and issuer.")
  except Exception:
    await channel.send("DEBUG: Token validation failed.")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed.")

async def fetch_user_profile(access_token: str):
  async with aiohttp.ClientSession() as session:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with session.get("https://graph.microsoft.com/v1.0/me") as response:
      if response.status != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch user profile.")
      user = await response.json()
    async with session.get("https://graph.microsoft.com/v1.0/me/photo/$value") as response:
      picture = await response.read() if response.status == 200 else None
    return {"email": user.get("mail"), "username": user.get("displayName"), "picture": picture}

@router.post("/auth/login")
async def handle_login(request: Request):
  app = request.app
  bot = app.state.discord_bot
  channel = bot.get_channel(bot.sys_channel)
  await channel.send("Auth Login processing...")

  data = await request.json()
  id_token = data.get("idToken")
  if not id_token:
    raise HTTPException(status_code=400, detail="ID Token is required.")

  access_token = data.get("accessToken")
  if not access_token:
    raise HTTPException(status_code=400, detail="Access Token is required.")

  client_id = app.state.microsoft_client_id
  payload = await verify_id_token(app, id_token, client_id)

  await channel.send("Process payload...")
  microsoft_id = payload.get("sub")
  if not microsoft_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

  access_token = payload.get("access_token")
  user_profile = await fetch_user_profile(access_token)

  user = await get_user_from_database(app, microsoft_id)
  if not user:
    async with app.state.db_pool.acquire() as conn:
      await conn.execute(
        """
          INSERT INTO users (guid, auth_info, email, username)
          VALUES ($1, $2, $3, $4)
          RETURNING id
        """,
        microsoft_id,
        payload,
        user_profile["email"],
        user_profile["username"]
      )
    user = {"email": user_profile["email"], "username": user_profile["username"]}
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

  token_data = {"sub": microsoft_id}
  token = jwt.encode(token_data, app.state.jwt_secret, algorithm=app.state.jwt_algorithm)

  return JSONResponse(content={"token": token, "profilePicture": user_profile["picture"], "username": user["username"]})

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