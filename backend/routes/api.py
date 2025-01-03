from fastapi import APIRouter, Request
from commands.image_commands import generate_and_upload_image

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
    print("image_generation")
    incoming_data = await request.json()

    app = request.app
    bot = app.state.discord_bot

    template_key = incoming_data.get("template", "default")
    user_input = incoming_data.get("userinput", "")
    selected_keys = incoming_data.get("keys", {})

    try:
        azure_image_url = await generate_and_upload_image(app, bot, template_key, selected_keys, user_input)
        return { "imageUrl": azure_image_url }
    except Exception as e:
        return {"error": str(e)}


