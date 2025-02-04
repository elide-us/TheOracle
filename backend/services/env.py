import os

def get_env_var(var_name: str) -> str:
  value = os.getenv(var_name)
  if not value:
    raise RuntimeError(f"ERROR: {var_name} missing.")
  return value

################################################################################
## API Bearer Tokens
################################################################################

def get_openai_token():
  return get_env_var("OPENAI_SECRET")

def get_discord_token():
  return get_env_var("DISCORD_SECRET")

def get_lumaai_token():
  return get_env_var("LUMAAI_SECRET")

################################################################################
## Discord Channel ID Numbers 
################################################################################

def get_system_channel() -> int:
  return int(get_env_var("DISCORD_SYSTEM_CHANNEL"))

################################################################################
## Azure Storage Account Configuration
################################################################################

def cdn_connection_string():
  return get_env_var("AZURE_BLOB_CONNECTION_STRING")

def cdn_container_name():
  return get_env_var("AZURE_BLOB_CONTAINER_NAME")

################################################################################
## Postgres SQL on Azure Configuration
################################################################################

def db_connection_string():
  return get_env_var("POSTGRES_CONNECTION_STRING")

################################################################################
## Microsoft Auth Service Configuration
################################################################################

def get_jwt_secret():
  return get_env_var("JWT_SECRET")

def get_ms_app_id():
  return get_env_var("AUTH_MICROSOFT_ID")

def get_discord_app_id():
  return get_env_var("AUTH_DISCORD_ID")
