import json, uuid

async def get_public_template(pool):
  result = {}
  async with pool.acquire() as conn:
    query = """
      WITH template_data AS (
        SELECT 
          c.name AS category,
          json_agg(
            json_build_object(
              'title', t.title,
              'description', t.description,
              'imageUrl', t.image_url,
              'layer1', t.layer1,
              'layer2', t.layer2,
              'layer3', t.layer3,
              'layer4', t.layer4,
              'input', t.input
            )
          ) AS templates
        FROM templates t
        JOIN categories c ON t.category_id = c.id
        GROUP BY c.name
      )
      SELECT json_object_agg(category, templates) AS result
      FROM template_data;
    """
    result = await conn.fetchval(query)
    if isinstance(result, str):
      result = json.loads(result)
  return result

async def get_layer_template(pool, layer_id):
  result = {}
  id = int(layer_id)
  async with pool.acquire() as conn:
    query = """
      SELECT jsonb_object_agg(key_value, subkeys) AS layer_data
      FROM (
        SELECT key_value, jsonb_object_agg(subkey_value, public_value) AS subkeys
        FROM keys
        WHERE layer = $1
        GROUP BY key_Value
      ) AS grouped;
    """
    result = await conn.fetchval(query, id)
    if isinstance(result, str):
      result = json.loads(result)
    return result

async def get_user_from_database(app, pool, microsoft_id):
  bot = app.state.discord_bot
  channel = bot.get_channel(bot.sys_channel)
  await channel.send("get_user_from_database()")
  async with pool.acquire() as conn:
    query = """
      SELECT guid, microsoft_id, email, username FROM users WHERE microsoft_id = $1
    """
    result = await conn.fetchrow(query, microsoft_id)
    if isinstance(result, str):
      result = json.loads(result)
    await channel.send(f"Result from select: {result}")
    return result
  
async def make_new_user_for_database(app, pool, microsoft_id, email, username):
  bot = app.state.discord_bot
  channel = bot.get_channel(bot.sys_channel)
  await channel.send("make_new_user_for_database()")

  new_guid = str(uuid.uuid4())
  await channel.send(f"No user found for Microsoft ID: {microsoft_id}")
  await channel.send(f"Creating new user with GUID: {new_guid}")
  async with pool.acquire() as conn:
    query = """
        INSERT INTO users (guid, microsoft_id, email, username)
        VALUES ($1, $2, $3, $4);
    """
    await conn.execute(query, new_guid, microsoft_id, email, username)
    await channel.send("Executed INSERT query")
    query = """
      SELECT guid, microsoft_id, email, username FROM users WHERE microsoft_id = $1
    """
    result = await conn.fetchrow(query, microsoft_id)
    if isinstance(result, str):
      result = json.loads(result)
    await channel.send(f"Result from insert-select: {result}")
    return result