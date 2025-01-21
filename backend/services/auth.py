import aiohttp, base64, jwt
from fastapi import HTTPException, status
from typing import Dict

async def fetch_openid_config(app):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://login.microsoftonline.com/consumers/v2.0/.well-known/openid-configuration") as response:
      if response.status != 200:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Failed to fetch OpenID configuration.")
      openid_config = await response.json()
      app.state.jwks_url = openid_config["jwks_uri"]

async def fetch_jwks(app): 
  async with aiohttp.ClientSession() as session:
    async with session.get(app.state.jwks_url) as response:
      if response.status != 200:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Failed to fetch JWKS.")
      app.state.jwks = await response.json()

async def get_jwks(app):
  if not hasattr(app.state, "jwks") or not app.state.jwks:
    if not hasattr(app.state, "jwks_uri"):
      await fetch_openid_config(app)
    await fetch_jwks(app)
  return app.state.jwks

################################################################################
## Public API
################################################################################

async def verify_id_token(state, ms_id_token: str) -> Dict:
  jwks = await get_jwks(state.app)

  try:
    unverified_header = jwt.get_unverified_header(ms_id_token)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid ID token.")

  rsa_key = next(
    (
      {
        "kty": key["kty"],
        "kid": key["kid"],
        "use": key["use"],
        "n": key["n"],
        "e": key["e"],
      }
      for key in jwks["keys"]
      if key["kid"] == unverified_header["kid"]
    ),
    None,
  )
  if not rsa_key:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header.")
  
  try:
    payload = jwt.decode(
      ms_id_token,
      rsa_key,
      algorithms=["RS256"],
      audience=state.ms_api_id,
      issuer="https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/v2.0"
    )
    return payload
  
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
  except jwt.JWTClaimsError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect claims. Please check the audience and issuer.")
  except Exception:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed.")

async def fetch_user_profile(access_token: str):
  async with aiohttp.ClientSession() as session:
    headers = {"Authorization": f"Bearer {access_token}"}

    async with session.get("https://graph.microsoft.com/v1.0/me", headers=headers) as response:
      if response.status != 200:
        error_message = await response.text()
        raise HTTPException(status_code=500, detail=f"Failed to fetch user profile. Status: {response.status}, Error: {error_message}")
      user = await response.json()
    
    # Fetch profile picture data
    profile_picture_bytes = None
    async with session.get("https://graph.microsoft.com/v1.0/me/photo/$value", headers=headers) as response:
      if response.status == 200:
        profile_picture_bytes = await response.read()
        profile_picture_base64 = base64.b64encode(profile_picture_bytes).decode("utf-8")

    # Return structured user data
    return {
      "email": user.get("mail") or user.get("userPrincipalName"),  # Handle fallback for email
      "username": user.get("displayName"),
      "profilePicture": profile_picture_base64
    }