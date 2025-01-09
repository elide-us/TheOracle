from fastapi import APIRouter, Request
from commands.image_commands import generate_and_upload_image
from commands.db_commands import get_public_template

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
    azure_image_url = await generate_and_upload_image(app, bot, template_key, selected_keys, user_input)
    return { "imageUrl": azure_image_url }
  except Exception as e:
    return {"error": str(e)}

@router.get("/imagen/{template_id}")
async def get_template(template_id: int, request: Request):
  match template_id:
    case 0:
      return None
    case _:
      return None
  
  result = await get_public_template(template_id, request.app.state.db_pool)
  return result

@router.get("/test-db")
async def test_db(request: Request):
  pool = request.app.state.db_pool
  async with pool.acquire() as conn:
    queryX = """
      WITH template_data AS (
        SELECT 
          c.name AS category,
          json_agg(
            json_build_object(
              'title', t.title,
              'description', t.description,
              'imageUrl', t.image_url,
              'layer1', t.layer1,
              'layer2', t.layer2,
              'layer3', t.layer3,
              'layer4', t.layer4,
              'input', t.input
            )
          ) AS templates
        FROM templates t
        JOIN categories c ON t.category_id = c.id
        GROUP BY c.name
      )
      SELECT json_object_agg(category, templates) AS result
      FROM template_data;
    """
    query = """
      SELECT json_build_object(
        'key', 'value'
      ) AS result;
    """
    result = await conn.fetchval(query)
  return {"queryResult": result}

# @router.get("/lumagen")
# async def video_generation(request: Request):
#     incoming_data = await request.json()

#     app = request.app
#     bot = app.state.discord_bot

#     return None

@router.get("/test-db2")
async def test_db(request: Request):
  pool = request.app.state.db_pool
  async with pool.acquire() as conn:
    query = """
      SELECT json_agg(
        json_build_object('title', t.title)
      ) AS result
      FROM templates t;
    """
    result = await conn.fetchval(query)
  return {"queryResult": result}
