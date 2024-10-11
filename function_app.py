import azure.functions as func
import logging
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Setup environment variables
KEY_VAULT_NAME = os.getenv("KEY_VAULT_NAME")

# Use DefaultAzureCredential for authentication
credential = DefaultAzureCredential()
key_vault_uri = f"https://{KEY_VAULT_NAME}.vault.azure.net"
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

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

    # Retrieve a secret from Key Vault
    try:
        secret_name = "test-key"
        retrieved_secret = secret_client.get_secret(secret_name)
        secret_value = retrieved_secret.value
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