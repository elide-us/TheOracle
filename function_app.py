# import azure.functions as func
# import logging

# from azure.identity import ClientSecretCredential
# from azure.keyvault.secrets import SecretClient
# from msal import ConfidentialClientApplication
# import os

# # Define configuration for MSAL and Azure Key Vault
# CLIENT_ID = os.getenv("THEORACLEKV_CLIENT_ID")
# CLIENT_SECRET = os.getenv("THEORACLEKV_CLIENT_SECRET")
# TENANT_ID = os.getenv("TENANT_ID")
# KEY_VAULT_URL = os.getenv("THEORACLEKV_URL")
# AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# SCOPE = ["https://vault.azure.net/.default"]

# # Initialize MSAL Confidential Client Application for OAuth2.0 authentication
# msal_app = ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

# # Initialize the Azure Function app
# app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
# @app.route(route="HttpExample")
# def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     # Get the "name" parameter from the request
#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     # Acquire a token using MSAL
#     try:
#         result = msal_app.acquire_token_for_client(scopes=SCOPE)
#         if "access_token" not in result:
#             raise Exception("Could not obtain access token")
#         access_token = result["access_token"]
#     except Exception as e:
#         logging.error(f"Failed to obtain access token: {str(e)}")
#         return func.HttpResponse(
#             "Error: Unable to obtain access token.",
#             status_code=500
#         )

#     # Initialize SecretClient using the Key Vault URL and the access token
#     credential = ClientSecretCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
#     secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

#     # Retrieve a test value from Azure Key Vault
#     secret_name = "test-key"  # Assuming "test-key" is the name of your secret
#     try:
#         secret = secret_client.get_secret(secret_name)
#         secret_value = secret.value
#         logging.info(f'Successfully retrieved secret: {secret_name}')
#     except Exception as e:
#         logging.error(f'Failed to retrieve secret: {str(e)}')
#         return func.HttpResponse(
#             "Error: Unable to retrieve the secret from Key Vault.",
#             status_code=500
#         )

#     # Create response based on whether "name" parameter was provided
#     if name:
#         response_message = (f"Hello, {name}. This HTTP triggered function executed successfully. "
#                             f"Retrieved secret value is: {secret_value}")
#     else:
#         response_message = (f"This HTTP triggered function executed successfully. Retrieved secret value is: {secret_value}. "
#                             "Pass a name in the query string or in the request body for a personalized response.")

#     return func.HttpResponse(response_message, status_code=200)



import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )