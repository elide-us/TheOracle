from typing import Any
from fastapi import Request
import aiohttp, io, aiofiles, json

async def load_json(file_path: str) -> Any:
  try:
    async with aiofiles.open(file_path, mode='r') as file:
      return json.loads(await file.read())
  except FileNotFoundError:
    return None

class StateHelper:
  def __init__(self, request: Request):
    self.request = request
  #   self.__state = request.app.state
  # def __getattr__(self, name):
  #   getattr(self.__state, name)
  @property
  def app(self) -> Any:
    return self.request.app
  @property
  def bot(self) -> Any:
    return self.request.app.state.discord_bot
  @property
  def channel(self) -> Any:
    return self.bot.get_channel(self.bot.sys_channel)
  @property
  def pool(self) -> Any:
    return self.request.app.state.theoraclegp_pool
  @property
  def ms_api_id(self) -> Any:
    return self.request.app.state.ms_app_id
  @property
  def jwt_secret(self) -> Any:
    return self.request.app.state.jwt_secret
  @property
  def jwt_algo_ms(self) -> Any:
    return self.request.app.state.jwt_algorithm_rs256
  @property
  def jwt_algo_int(self) -> Any:
    return self.request.app.state.jwt_algorithm_hs256
  @property
  def ms_jwks(self):
    return self.request.app.state.ms_jwks
  @property
  def storage(self):
    return self.request.app.state.theoraclesa_client
  @property
  def openai(self):
    return self.request.app.state.openai_client
  
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

class SafeDict(dict):
    def __missing__(self, key):
        return ''