import asyncpg
from config import get_db_password

async def get_db_client():
  pw = get_db_password()
  pool = await asyncpg.create_pool(
    dsn=f"postgresql://theoracleadmin:{pw}@theoraclepg.postgres.database.azure.com:5432/theoraclegpt?sslmode=require",
  )
  return pool