from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/files")
async def list_files(request: Request):
  container_client = request.app.state.container_client
  blobs = []
  async for blob in container_client.list_blobs():
    blobs.append(blob.name)
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