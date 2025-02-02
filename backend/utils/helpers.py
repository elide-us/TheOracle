from typing import Any
from fastapi import Request
import aiohttp, io, aiofiles, json

# A temporary helper function to load local data JSON files
async def load_json(file_path: str) -> Any:
  try:
    async with aiofiles.open(file_path, mode='r') as file:
      return json.loads(await file.read())
  except FileNotFoundError:
    return None

# Shortcut class for various objects commonly used on the app.state object
class StateHelper:
  def __init__(self, app: Any):
    self._app = app
  @classmethod
  def from_request(cls, request: Request):
    return cls(request.app)
  @classmethod
  def from_context(cls, ctx: Any):
    return cls(ctx.bot.app)
  @property
  def app(self) -> Any:
    return self._app
  @property
  def bot(self) -> Any:
    return self.app.state.discord_bot
  @property
  def channel(self) -> Any:
    return self.bot.get_channel(self.bot.sys_channel)
  @property
  def pool(self) -> Any:
    return self.app.state.theoraclegp_pool
  @property
  def ms_api_id(self) -> Any:
    return self.app.state.ms_app_id
  @property
  def jwt_secret(self) -> Any:
    return self.app.state.jwt_secret
  @property
  def jwt_algo_ms(self) -> Any:
    return self.app.state.jwt_algorithm_rs256
  @property
  def jwt_algo_int(self) -> Any:
    return self.app.state.jwt_algorithm_hs256
  @property
  def ms_jwks(self):
    return self.app.state.ms_jwks
  @property
  def storage(self):
    return self.app.state.theoraclesa_client
  @property
  def openai(self):
    return self.app.state.openai_client
  
# Async Context Manager for buffer
class AsyncBufferWriter():
  def __init__(self, url):
    self.buffer = None
    self.url = url

  async def __aenter__(self):
    self.buffer = await self._fetch_buffer()
    return self.buffer
  
  async def _fetch_buffer(self):
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(self.url) as response:
          response.raise_for_status()
          return io.BytesIO(await response.read())
    except aiohttp.ClientError as e:
      raise ValueError(f"Failed to fetch buffer from {self.url}: {str(e)}")

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    if self.buffer:
      self.buffer.close()

# A safe filter for dictionary keys that might be null
class SafeDict(dict):
    def __missing__(self, key):
        return ''