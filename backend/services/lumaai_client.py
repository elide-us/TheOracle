from lumaai import AsyncLumaAI, LumaAI
from config import get_lumaai_token

async def init_lumaai_client():
  token = get_lumaai_token()
  return AsyncLumaAI(auth_token=token)
