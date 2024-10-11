import azure.functions as func
import logging
import msal
import os

CLIENT_ID = os.getenv("THEORACLE_CLIENT_ID")
TENANT_ID = os.getenv("THEORACLE_TENANT_ID")
CLIENT_SECRET = os.getenv("THEORACLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("THEORACLE_REDIRECT_URI")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = [
    "User.Read",
    "Mail.Read",
    "Mail.TedaBasic",
    "Mail.ReadWrite",
    "Mail.Send"
]

def create_msal_app():
    return msal.ConfidentialClientApplication(client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY)

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
