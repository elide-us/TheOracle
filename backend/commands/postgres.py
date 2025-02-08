import json
from uuid import uuid4
from typing import Dict
from utils.helpers import StateHelper, stou, utos, maybe_loads_json
from utils.messaging import send_to_discord

# Use to get complex data
async def database_fetch_many(state: StateHelper, query: str, *args):
  async with state.pool.acquire() as conn:
    result = await conn.fetchval(query, *args)
    return maybe_loads_json(result)

# Use to get one row of data
async def database_fetch_one(state: StateHelper, query: str, *args):
  async with state.pool.acquire() as conn:
    result = await conn.fetchrow(query, *args)
    return maybe_loads_json(result)

# Use for UPDATE, CREATE, etc.
async def database_run(state: StateHelper, query: str, *args):
  async with state.pool.acquire() as conn:
    await conn.execute(query, *args)
  return None

# Use to get complex data with a user's bearer token guid
async def database_secure_fetch_many(state: StateHelper, query: str, sub: str, *args):
  async with state.pool.acquire() as conn:
    sub_uuid = stou(sub)
    result = await conn.fetchval(query, sub_uuid, *args)
    return maybe_loads_json(result)

# Use to get one row of data with a user's bearer token guid
async def database_secure_fetch_one(state: StateHelper, query: str, sub: str, *args):
  async with state.pool.acquire() as conn:
    sub_uuid = stou(sub)
    result = await conn.fetchrow(query, sub_uuid, *args)
    return maybe_loads_json(result)

# Use for UPDATE, CREATE, etc. with a user's bearer token guid
async def database_secure_run(state: StateHelper, query: str, sub: str, *args):
  async with state.pool.acquire() as conn:
    sub_uuid = stou(sub)
    await conn.execute(query, sub_uuid, *args)
  return None

################################################################################
## Database Queries for the Prompt Builder
################################################################################

# Returns the prompt text elements for the selected keys
async def select_prompt_keys(state: StateHelper, selected_keys: Dict[str, str]) -> Dict[str, str]:
  elements = {}
  query = """
    SELECT jsonb_object_agg(key_value, sub_data) 
    FROM (
      SELECT key_value, jsonb_object_agg(subkey_value, private_value) AS sub_data
      FROM keys
      WHERE (key_value, subkey_value) IN (
        SELECT unnest($1::text[]), unnest($2::text[])
      )
      GROUP BY key_value
    ) AS nested_data;
  """
  keys = list(selected_keys.keys())
  await state.channel.send(f"Keys: {keys}")
  subkeys = list(selected_keys.values())
  await state.channel.send(f"Subkeys: {subkeys}")

  result = await database_fetch_many(state, query, keys, subkeys)
  if result is None:
    raise ValueError("No matching elements in the database.")

  for key, subkey in selected_keys.items():
    if key in result and subkey in result[key]:
      elements[key] = result[key][subkey]
    else:
      raise ValueError(f"Key '{subkey}' not found under '{key}' in database.")

  return elements

# Returns the categorized templates list
async def select_category_templates(state: StateHelper):
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
  return await database_fetch_many(state, query)

# Returns the keys for a selected template
async def select_template_keys(state: StateHelper, layer):
  id = int(layer)
  query = """
    SELECT jsonb_object_agg(key_value, subkeys) AS layer_data
    FROM (
      SELECT key_value, jsonb_object_agg(subkey_value, public_value) AS subkeys
      FROM keys
      WHERE layer = $1
      GROUP BY key_Value
    ) AS grouped;
  """
  return await database_fetch_many(state, query, id)

################################################################################
## Database Queries for Authentication
################################################################################

# Select user's guid and credit values from Microsoft user ID
async def select_ms_user(state: StateHelper, microsoft_id):
  async with state.pool.acquire() as conn:
    query = """
      SELECT 
        u.guid, 
        u.microsoft_id, 
        u.email, 
        u.username, 
        u.backup_email, 
        u.credits,
        p.name AS provider_name
      FROM users u
      JOIN auth_provider p
        ON u.default_provider = p.id
      WHERE u.microsoft_id = $1;
    """
    result = await conn.fetchrow(query, microsoft_id)
    if isinstance(result, str):
      result = json.loads(result)
      await state.channel.send(f"Found {result["provider_name"]} user for {result["guid"]}: {result["username"]}, {result["email"]}, Credits: {result["credits"]}")
    return result

# Create a user record with defaults for Microsoft user ID
async def insert_ms_user(state: StateHelper, microsoft_id, email, username):
  new_uuid = utos(uuid4())
  async with state.pool.acquire() as conn:
    query = """
      INSERT INTO users (guid, microsoft_id, email, username, security, credits)
      VALUES ($1, $2, $3, $4, 1, 50);
    """
    await conn.execute(query, new_uuid, microsoft_id, email, username)

    result = await select_ms_user(state, microsoft_id)
    await state.channel.send(f"Added user for {new_uuid}: {username}, {email}")
    return result

################################################################################
## Database Queries for User Profile
################################################################################

# Details appropriate for return to the front end
async def select_user_details(state: StateHelper, sub):
  try:
    sub_uuid = stou(sub)  # Ensure it's a UUID object
  except ValueError:
    await state.channel.send("Invalid GUID format")
    return {"error": "Invalid GUID format"}
  query = """
    SELECT u.username, u.email, u.backup_email, u.credits, ap.name AS provider_name
    FROM users u
    LEFT JOIN auth_provider ap ON u.default_provider = ap.id
    WHERE u.guid = $1
  """
  async with state.pool.acquire() as conn:
    result = await conn.fetchrow(query, sub_uuid)
    if isinstance(result, str):
      result = json.loads(result)
    return {
      "guid": utos(sub_uuid),
      "username": result.get("username", "No user found"),
      "email": result.get("email", "No email found"),
      "backup_email": result.get("backup_email", "No backup email found"),
      "credits": result.get("credits", 0),
      "default_provider": result.get("provider_name", "No provider found")
    }

# This should never be returned to the front end
async def select_user_security(state: StateHelper, sub):
  query = """
    SELECT security, guid FORM users WHERE guid = $1
  """
  async with state.pool.acquire() as conn:
    sub_uuid = stou(sub)
    result = await conn.fetchrow(query, sub_uuid)
    if isinstance(result, str):
      security = result["security"]
    if result:
      return {"security": security, "guid": utos(sub_uuid)}
    else:
      raise

################################################################################
## Database Commands for Front End "Routes" Object
################################################################################

# Returns routes that require no security, called when user is not logged in
async def select_public_routes(state: StateHelper):
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

# Returns routes based on security level
async def select_secure_routes(state: StateHelper, guid):
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

################################################################################
## Database Queries for Credits
################################################################################

# A transaction for getting and updating credits for a user
async def update_user_credits(state: StateHelper, charge: int, sub: str):
  query_select = """
    SELECT credits FROM users WHERE guid = $1
  """
  query_update = """
    UPDATE users SET credits = $1 WHERE guid = $2
  """
  async with state.pool.acquire() as conn:
    sub_uuid = stou(sub)
    async with conn.transaction():
      # Fetch the current credits
      result = await conn.fetchrow(query_select, sub_uuid)
      if isinstance(result, str):
        result = json.loads(result)
      if result:
        credits = result["credits"]
        if credits >= charge:
          # Deduct the charge
          new_credits = credits - charge
          # Update the database
          await conn.execute(query_update, new_credits, sub_uuid)
          return {"success": True, "credits": new_credits, "guid": utos(sub_uuid)}
        else:
          return {"success": False, "error": "Insufficient credits", "credits": credits, "guid": utos(sub_uuid)}
      else:
            return {"success": False, "error": "User not found", "guid": sub}

# A transaction for adding purchased credits for a user
async def update_user_credits_purchased(state: StateHelper, purchase: int, sub: str):
  query_select = """
    SELECT credits FROM users WHERE guid = $1
  """
  query_update = """
    UPDATE users SET credits = $1 WHERE guid = $2
  """
  async with state.pool.acquire() as conn:
    sub_uuid = stou(sub)
    async with conn.transaction():
      # Fetch the current credits
      result = await conn.fetchrow(query_select, sub_uuid)
      if isinstance(result, str):
        result = json.loads(result)
      if result:
        credits = result["credits"]
        new_credits = credits + purchase
        await conn.execute(query_update, new_credits, sub_uuid)
        return {"success": True, "credits": new_credits, "guid": utos(sub_uuid)}
      else:
        return {"success": False, "error": "User not found", "guid": sub}
