import os

def get_env_var(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"ERROR: {var_name} missing.")
    return value

def get_openai_token():
    return get_env_var("OPENAI_SECRET")

def get_discord_token():
    return get_env_var("DISCORD_SECRET")

def get_discord_channel() -> int:
    return int(get_env_var("DISCORD_CHANNEL"))

def get_lumaai_token():
    return get_env_var("LUMAAI_SECRET")

def get_blob_connection_string():
    return get_env_var("AZURE_BLOB_CONNECTION_STRING")

def get_blob_container():
    return get_env_var("AZURE_BLOB_CONTAINER_NAME")

def get_db_password():
    return get_env_var("PG_DB_PASSWORD")

def get_jwt_secret():
    return get_env_var("JWT_SECRET")

def get_microsoft_client_id():
    return get_env_var("APPREG_ID")