import os
import json
import requests
from flask import Flask, request, jsonify

DISCORD_TOKEN =  os.getenv('DISCORD_TOKEN')
WEBHOOK_ID = 1308553886868574409

WEBHOOK_URL = 'https://discordapp.com/api/webhooks/{WEBHOOK_ID}/{DISCORD_TOKEN}'

app = Flask(__name__)

def s_load_json(file_path):
  with open(file_path, "r") as file:
    data = json.load(file)
  return data

def send_discord_message(message):
  payload = {'content':'{message}'}
  response = requests.post(WEBHOOK_URL, json=payload)
  return response.status_code

@app.route('/webhook', methods=['POST'])
def handle_webhook():
  data = request.json
  if not data:
    return jsonify({'error':'Invalid payload'}), 400
  if "content" in data:
    received_message = data['content']
    send_discord_message({received_message})
  return jsonify({'status':'success'}), 200

if __name__ == '__main__':
  app.run(port=80)

