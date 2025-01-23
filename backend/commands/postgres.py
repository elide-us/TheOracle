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

async def get_database_user(state, microsoft_id):
  async with state.pool.acquire() as conn:
    query = """
      SELECT guid, microsoft_id, email, username FROM users WHERE microsoft_id = $1
    """
    result = await conn.fetchrow(query, microsoft_id)
    if isinstance(result, str):
      result = json.loads(result)
    return result
  
async def make_database_user(state, microsoft_id, email, username):
  new_guid = str(uuid.uuid4())
  async with state.pool.acquire() as conn:
    query = """
        INSERT INTO users (guid, microsoft_id, email, username)
        VALUES ($1, $2, $3, $4);
    """
    await conn.execute(query, new_guid, microsoft_id, email, username)

    result = await get_database_user(state, microsoft_id)
    return result

# New code below

async def verify_user_token_in_database(state, bearer_token, guid):
  channel = state.channel
  await channel.send("Verify User Token in Database")

  async with state.pool.acquire() as conn:
    query = """
      SELECT microsoft_id FROM users WHERE guid = $1;
    """
    select = await conn.fetch(query, guid)
    if isinstance(select, str):
      select = json.loads(select)

    # Extract "sub" and validate against app.store.jwks
  return select

async def charge_user_for_access(state, bearer_token, guid, charge):
  channel = state.channel
  await channel.send("Charge User for Access")

  # if id < 20 = free

  return None