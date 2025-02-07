from fastapi import APIRouter, Request, Depends
from commands.openai import generate_image
from commands.video_commands import download_generation
from commands.postgres import select_category_templates, select_template_keys, select_ms_user, insert_ms_user, select_public_routes, select_secure_routes, update_user_credits
from services.auth import handle_ms_auth_login, make_bearer_token, get_bearer_token_payload
from utils.helpers import StateHelper

router = APIRouter()

@router.get("/routes")
async def get_routes(request: Request, payload: dict = Depends(get_bearer_token_payload)):
  state = StateHelper.from_request(request)
  await state.channel.send("routes")

  user_guid = payload.get("guid")
  if user_guid:
    await state.channel.send("with guid")
    secure_routes = await select_secure_routes(state, user_guid)
    if secure_routes:
      await state.channel.send("with secure")
      return secure_routes
    
    await state.channel.send("without secure")
    return {"routes": [{'/', 'Home', 'home'}]}
  else:
    public_routes = await select_public_routes(state)
    await state.channel.send("with public")
    return public_routes

@router.post("/lumaai")
async def post_lumaai(request: Request):
  state = StateHelper.from_request(request)
  generation = await request.json()
  if generation.get("state") == "completed":
    video_url = generation.get("assets", {}).get("video")
    filename = f"{generation.get("id")}.mp4"
    await download_generation(video_url, state, filename)
  else:
    await state.out_channel.send("Dreaming...")

@router.get("/userpage")
async def get_userpage(request: Request, payload: dict = Depends(get_bearer_token_payload)):
  state = StateHelper.from_request(request)
  await state.channel.send("get_userpage")

  # guid = payload.get("guid")
  # username = payload.get("username")
  # email = payload.get("email")
  # backupEmail = payload.get("backup_email")
  # credits = payload.get("credits")
  # defaultProvider = payload.get("default_provider")

  return payload

@router.post("/userpage")
async def post_userpage(request: Request, payload: dict = Depends(get_bearer_token_payload)):
  state = StateHelper.from_request(request)
  await state.channel.send("post_userpage")

  # defaultProvider
  # username
  # email
  # backupEmail

  # update default_provider, etc. from form data

  return None
  
@router.post("/userpage/link")
async def post_userpage_link(request: Request, payload: dict = Depends(get_bearer_token_payload)):
  state = StateHelper.from_request(request)
  await state.channel.send("post_userpage_link")
  
  # popup user login, capture accessToken and idToken
  # decode and validate idToken
  # get profile data
  # create a users_auth entry for guid + unique_id + username + email
  # update users record for id from users_auth

  return None

@router.post("/userpage/unlink")
async def post_userpage_link(request: Request, payload: dict = Depends(get_bearer_token_payload)):
  state = StateHelper.from_request(request)
  await state.channel.send("post_userpage_unlink")
  
  # check if this is the last provider, ask if they wish to delete their account
  # delete row by guid and provider unique select

  return None  

@router.post("/auth/login/ms")
async def post_auth_login_ms(request: Request):
  state = StateHelper.from_request(request)

  unique_identifier, ms_profile = await handle_ms_auth_login(request)

  user = await select_ms_user(state, unique_identifier)
  if not user:
    user = await insert_ms_user(state, unique_identifier, ms_profile["email"], ms_profile["username"])

  return {
    "bearerToken": make_bearer_token(state, str(user["guid"])),
    "defaultProvider": user["provider_name"],
    "username": user["username"],
    "email": user["email"],
    "backupEmail": user["backup_email"],
    "profilePicture": ms_profile["profilePicture"],
    "credits": user["credits"]
  }

@router.get("/files")
async def get_files(request: Request):
  state = StateHelper.from_request(request)

  base_url = f"https://theoraclesa.blob.core.windows.net/{state.storage.container_name}/"  # Replace with your actual base URL
  blobs = []
  async for blob in state.storage.list_blobs():
    blobs.append({
      "name": blob.name,
      "url": f"{base_url}{blob.name}"
    })
  return {"files": blobs}

# @router.delete("/files/{filename}")
# async def delete_file(filename: str, request: Request, token: str = Depends(HTTPBearer())):
#   state = StateHelper(request)
#   container_client = request.app.state.container_client
#   await container_client.delete_blob(filename)
#   return {"status": "deleted", "file": filename}

# @router.post("/files")
# async def upload_file(filename: str, request: Request, token: str = Depends(HTTPBearer()):
#   state = StateHelper(request)
#   container_client = request.app.state.container_client
#   await container_client.upload_blob(filename)
#   return {"status": "uploaded", "file": filename}


@router.post("/imagen")
async def post_imagen(request: Request, payload: dict = Depends(get_bearer_token_payload)):
  state = StateHelper.from_request(request)

  charge = 5
  credits = payload.get("credits")

  if credits > charge:
    response = await update_user_credits(state, charge, payload.get("guid"))
    if response["success"]:
      await state.channel.send(f"User: {response["guid"]} Credits: {response['credits']}")
    else:
      await state.channel.send(f"Error: {response['error']}, Remaining credits: {response.get('credits', 0)}")

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
async def get_imagen_template_id(template_id: int, request: Request):
  state = StateHelper.from_request(request)

  match template_id:
    case 0:
      return await select_category_templates(state.pool)
    case 1:
      return await select_template_keys(state.pool, 1)
    case 2:
      return await select_template_keys(state.pool, 2)
    case 3:
      return await select_template_keys(state.pool, 3)
    case 4:
      return await select_template_keys(state.pool, 4)
    case _:
      return {}

# @router.post("/lumagen")
# async def video_generation(request: Request):
#     incoming_data = await request.json()

#     app = request.app
#     bot = app.state.discord_bot

#     return None