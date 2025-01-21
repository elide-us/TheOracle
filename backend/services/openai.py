from openai import AsyncOpenAI
from conf.env import get_openai_token

async def init_openai_client():
    token = get_openai_token()
    return AsyncOpenAI(api_key=token)