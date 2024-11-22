import os
from flask import Flask

DISCORD_SECRET = os.getenv('DISCORD_SECRET')
OPENAI_SECRET = os.getenv('OPENAI_SECRET')
LUMAAI_SECRET = os.getenv('LUMAAI_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')

app = Flask(__name__, host="0.0.0.0", port=80)

@app.route('/')
def index():
  return "{TENANT_ID"
