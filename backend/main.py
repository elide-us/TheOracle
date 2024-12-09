from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import api, web
from lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api.router, prefix="/api")
app.include_router(web.router)

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running with a Discord bot!"}
