from openai import AsyncOpenAI
from config.env import get_openai_token

async def init_openai_client():
    token = get_openai_token()
    return AsyncOpenAI(api_key=token)