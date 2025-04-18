import aiohttp, base64
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Dict
from utils.helpers import StateHelper
from commands.postgres import select_user_details

################################################################################
## Microsoft Authentication Setup
################################################################################

# Gets the Microsoft RSA public JWKS URL
async def fetch_ms_jwks_uri():
  async with aiohttp.ClientSession() as session:
    async with session.get("https://login.microsoftonline.com/consumers/v2.0/.well-known/openid-configuration") as response:
      if response.status != 200:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Failed to fetch OpenID configuration.")
      response_data = await response.json()
      return response_data["jwks_uri"]

# Gets the Microsoft RSA public JWKS
async def fetch_ms_jwks(jwks_uri):
  async with aiohttp.ClientSession() as session:
    async with session.get(jwks_uri) as response:
      if response.status != 200:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Failed to fetch JWKS.")
      response_data = await response.json()
      return response_data

################################################################################
## Internal Functions for Microsoft Authentication
################################################################################

# Verifies a JWT against the Microsoft public RSA keys
async def verify_ms_id_token(state: StateHelper, id_token: str) -> Dict:
  try:
    unverified_header = jwt.get_unverified_header(id_token)
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
      for key in state.ms_jwks["keys"]
      if key["kid"] == unverified_header["kid"]
    ),
    None,
  )
  if not rsa_key:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header.")
  
  try:
    payload = jwt.decode(
      id_token,
      rsa_key,
      algorithms=[state.jwt_algo_ms],
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

# Uses an access token to retrieve user details for a Microsoft Account
async def fetch_ms_user_profile(access_token: str):
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

# Verifies and downloads the profile of a Microsoft Account user
async def handle_ms_auth_login(request: Request):
  state = StateHelper.from_request(request)

  request_data = await request.json()

  id_token = request_data.get("idToken")
  if not id_token:
    raise HTTPException(status_code=400, detail="ID Token is required.")

  payload = await verify_ms_id_token(state, id_token)

  unique_identifier = payload.get("sub")
  if not unique_identifier:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

  access_token = request_data.get("accessToken")
  if not access_token:
    raise HTTPException(status_code=400, detail="Access Token is required.")

  ms_profile = await fetch_ms_user_profile(access_token)

  await state.channel.send(f"Processing login for: {ms_profile["username"]}, {ms_profile["email"]}")

  return unique_identifier, ms_profile

################################################################################
## Intrnal Authentication Functions
################################################################################

# Encodes a JWT against our internal user GUID
def make_bearer_token(state: StateHelper, guid: str):
  exp = datetime.now(timezone.utc) + timedelta(hours=24)
  token_data = {"sub": guid, "exp": exp.timestamp()}
  token = jwt.encode(token_data, state.jwt_secret, algorithm=state.jwt_algo_int)
  return token

# Decodes a JWT against our internal secret
async def decode_bearer_token(state: StateHelper, token: str):
  try:
    payload = jwt.decode(token, state.jwt_secret, algorithms=[state.jwt_algo_int])
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
  
  exp = payload.get("exp")
  if not exp:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expiry not found", headers={"WWW-Authenticate": "Bearer"})
  if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})

  sub = payload.get("sub")
  if not sub:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Subject not found", headers={"WWW-Authenticate": "Bearer"})

  details = await select_user_details(state, sub)
  await state.channel.send(f"Details: {details}")
  return details

# Provides a decode of the token for certain API calls that require validating credits or security before execution
async def get_bearer_token_payload(request: Request, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
  state = StateHelper.from_request(request)
  return await decode_bearer_token(state, token.credentials)
