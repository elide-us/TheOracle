from typing import Any
from fastapi import Request, HTTPException

class TokenHelper:
  def __init__(self, request: Request):
    self._request = request
    self._json_data = None
  async def _get_json_data(self) -> dict:
    if self._json_data is None:
      self._json_data = await self._request.json()
    return self._json_data
  async def get_token(self, token_name: str) -> Any:
    data = await self._get_json_data()
    token = data.get(token_name)
    if not token:
      raise HTTPException(status_code=400, detail=f"{token_name} is required.")
    return token
  async def id_token(self) -> str:
    return await self.get_token("idToken")
  async def access_token(self) -> str:
    return await self.get_token("accessToken")

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
    return self.request.app.state.db_pool
  @property
  def ms_api_id(self) -> Any:
    return self.request.app.state.microsoft_client_id
  @property
  def jwt_secret(self) -> Any:
    return self.request.app.state.jwt_secret
  @property
  def jwt_algorithm(self) -> Any:
    return self.request.app.state.jwt_algorithm
  @property
  def ms_jwks(self):
    return self.request.app.state.ms_jwks # impl lazy loader
  @property
  def storage(self):
    return self.request.app.state.container_client