from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.rpc_discord import router as rpc_discord_router
from routes.api import router as legacy_api_router
from routes.web import router as react_router
from lifespan import lifespan

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(legacy_api_router)
app.include_router(react_router)
app.include_router(rpc_discord_router)

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running with a Discord bot!"}
