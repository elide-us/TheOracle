from lumaai import AsyncLumaAI, LumaAI
from conf.env import get_lumaai_token

async def init_lumaai_client():
  token = get_lumaai_token()
  return LumaAI(auth_token=token)

