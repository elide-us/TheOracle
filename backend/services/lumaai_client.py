from lumaai import AsyncLumaAI, LumaAI
from config import get_lumaai_token

async def init_lumaai():
  token = await get_lumaai_token()
  return LumaAI(auth_token=token)