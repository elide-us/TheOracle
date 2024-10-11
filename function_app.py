import azure.functions as func
import logging
import os
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Setup environment variables
CLIENT_ID = os.getenv("THEORACLE_CLIENT_ID")
TENANT_ID = os.getenv("THEORACLE_TENANT_ID")
CLIENT_SECRET = os.getenv("THEORACLE_CLIENT_SECRET")
KEY_VAULT_NAME = os.getenv("KEY_VAULT_NAME")

@app.function_name(name="StartLogin")
@app.route(route="start-login")
def start_login(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    # Retrieve a secret from Key Vault using REST API
    try:
        vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
        token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        resource = "https://vault.azure.net"
        
        # Get access token
        token_response = requests.post(token_url, data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': resource + '/.default'
        })
        token_response.raise_for_status()
        access_token = token_response.json().get('access_token')
        
        # Get secret from Key Vault
        secret_name = "your-secret-name"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        secret_response = requests.get(f"{vault_url}/secrets/{secret_name}?api-version=7.2", headers=headers)
        secret_response.raise_for_status()
        secret_value = secret_response.json().get('value')
        logging.info(f"Retrieved secret value: {secret_value}")
    except Exception as e:
        logging.error(f"Failed to retrieve secret from Key Vault: {e}")
        secret_value = "Unable to retrieve secret"

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. Secret Value: {secret_value}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )