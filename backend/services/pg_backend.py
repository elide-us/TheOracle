import asyncpg
from config import get_db_password

async def get_db_client():
  pw = get_db_password()
  conn = await asyncpg.create_pool(
    user="theoracleadmin",
    password=pw,
    host="theoraclepg.postgres.database.azure.com",
    port=5432,
    database="theoraclegpt"
  )
  return conn