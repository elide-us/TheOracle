from typing import Any
from fastapi import Request

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
    return self.request.app.state.ms_app_id
  @property
  def jwt_secret(self) -> Any:
    return self.request.app.state.jwt_secret
  @property
  def jwt_algorithm(self) -> Any:
    return self.request.app.state.jwt_algorithm
  @property
  def ms_jwks(self):
    return self.request.app.state.ms_jwks
  @property
  def storage(self):
    return self.request.app.state.container_client