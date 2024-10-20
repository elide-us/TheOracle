import azure.functions as func
import logging
import os
import requests
from openai import OpenAI

# Define the OpenAI API endpoint and environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = "https://api.openai.com/v1/completions"

def summarize_email(json, config):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Summarize the following text:\n\n{json}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful note taking assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="TheOracle")
@app.route(route="the-oracle")
def the_oracle(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  # Get name from query parameters or request body
  name = req.params.get('Enter your query here...')
  if not name:
    try:
      req_body = req.get_json()
    except ValueError:
      pass
    else:
      name = req_body.get('name')

  if name:
    # Make a request to OpenAI API using the name as the query
    prompt = f"Passing {name} to OpenAI."

    # Construct the payload for OpenAI API
    openai_data = {
      "model": "text-davinci-003",
      "prompt": prompt,
      "max_tokens": 50,
      "temperature": 0.7
    }

    headers = {
      "Authorization": f"Bearer {OPENAI_API_KEY}",
      "Content-Type": "application/json"
    }

    try:
      # Send a POST request to OpenAI API
      response = requests.post(OPENAI_API_URL, headers=headers, json=openai_data)

      if response.status_code == 200:
        response_json = response.json()
        completion = response_json['choices'][0]['text'].strip()

        return func.HttpResponse(f"OpenAI Response: {completion}", status_code=200)
      else:
        logging.error(f"OpenAI API call failed: {response.status_code} - {response.text}")
        return func.HttpResponse(f"OpenAI API call failed with status code {response.status_code}.", status_code=500)
    except Exception as e:
      logging.error(f"Error calling OpenAI API: {e}")
      return func.HttpResponse(f"Error calling OpenAI API: {e}", status_code=500)

  else:
    return func.HttpResponse(
      "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
      status_code=200
    )