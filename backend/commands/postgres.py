import json, uuid
from utils.helpers import StateHelper

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

async def get_database_user(state: StateHelper, microsoft_id):
  async with state.pool.acquire() as conn:
    query = """
      SELECT guid, microsoft_id, email, username, credits
      FROM users
      WHERE microsoft_id = $1
    """
    result = await conn.fetchrow(query, microsoft_id)
    if isinstance(result, str):
      result = json.loads(result)
      await state.channel.send(f"Found user for {result["guid"]}: {result["username"]}, {result["email"]}, Credits: {result["credits"]}")
    return result
  
async def make_database_user(state: StateHelper, microsoft_id, email, username):
  new_guid = str(uuid.uuid4())
  async with state.pool.acquire() as conn:
    query = """
      INSERT INTO users (guid, microsoft_id, email, username, security, credits)
      VALUES ($1, $2, $3, $4, 1, 50);
    """
    await conn.execute(query, new_guid, microsoft_id, email, username)

    result = await get_database_user(state, microsoft_id)
    await state.channel.send(f"Added user for {new_guid}: {username}, {email}")
    return result

async def get_details_for_user(state: StateHelper, sub):
  try:
    sub_uuid = uuid.UUID(sub)  # Ensure it's a UUID object
  except ValueError:
    await state.channel.send("Invalid GUID format")
    return {"error": "Invalid GUID format"}
  query = """
    SELECT credits FROM users WHERE guid = $1
  """
  async with state.pool.acquire() as conn:
    result = await conn.fetchrow(query, sub_uuid)
    if isinstance(result, str):
      result = json.loads(result)
    if result:
      return {"credits": result["credits"], "guid": str(sub_uuid)}
    else:
      return {"credits": 0, "guid": str(sub_uuid)}

async def get_security_for_user(state: StateHelper, sub):
  query = """
    SELECT security, guid FORM users WHERE guid = $1
  """
  async with state.pool.acquire() as conn:
    uuid_sub = uuid.UUID(sub)
    result = await conn.fetchrow(query, uuid_sub)
    if isinstance(result, str):
      security = result["security"]
    if result:
      return {"security": security, "guid": sub}
    else:
      raise

async def get_public_routes(state: StateHelper):
  query = """
    SELECT json_agg(
      json_build_object('path', path, 'name', name, 'icon', icon)
    ) AS routes
    FROM (
      SELECT path, name, icon 
      FROM routes 
      WHERE security < 1 
      ORDER BY sequence) subquery;
  """
  async with state.pool.acquire() as conn:
    result = await conn.fetch(query)
    if isinstance(result, str):
      result = json.loads(result)
    return result or None
  
async def get_secure_routes(state: StateHelper, guid):
  query = """
    SELECT json_agg(
      json_build_object(
        'path', r.path,
        'name', r.name,
        'icon', r.icon
        )
    ) AS routes
    FROM (
      SELECT r.path, r.name, r.icon
      FROM routes r
      JOIN users u ON u.guid = $1
      WHERE r.security < u.security
      ORDER BY r.sequence
    ) subquery;
  """
  async with state.pool.acquire() as conn:
    result = await conn.fetch(query, guid)
    if isinstance(result, str):
      result = json.loads(result)
    return result or None
  
async def charge_user_credits(state: StateHelper, charge: int, guid: str):
  query_select = """
    SELECT credits FROM users WHERE guid = $1
  """
  query_update = """
    UPDATE users SET credits = $1 WHERE guid = $2
  """
  async with state.pool.acquire() as conn:
    uuid_guid = uuid.UUID(guid)
    async with conn.transaction():
      # Fetch the current credits
      result = await conn.fetchrow(query_select, uuid_guid)
      if isinstance(result, str):
        result = json.loads(result)
      if result:
        credits = result["credits"]
        if credits >= charge:
          # Deduct the charge
          new_credits = credits - charge
          # Update the database
          await conn.execute(query_update, new_credits, uuid_guid)
          return {"success": True, "credits": new_credits, "guid": guid}
        else:
          return {"success": False, "error": "Insufficient credits", "credits": credits, "guid": guid}
      else:
            return {"success": False, "error": "User not found", "guid": guid}
