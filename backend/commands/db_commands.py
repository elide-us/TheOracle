import json

async def db_get_public(conn):
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
  if result is None:
    result = {}
  result_dict = json.loads(result)
  return result_dict


async def get_public_template(id, pool):
  async with pool.acquire() as conn:
    match id:
      case 0:
        return db_get_public(conn)
      case _:
        return None
