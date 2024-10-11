import azure.functions as func
import logging
# import msal
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="StartLogin")
@app.route(route="start-login")
def start_login(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    CLIENT_ID = os.getenv("THEORACLE_CLIENT_ID")
    TENANT_ID = os.getenv("THEORACLE_TENANT_ID")
    CLIENT_SECRET = os.getenv("THEORACLE_CLIENT_SECRET")
    # AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

    # REDIRECT_URI = "https://theoraclefn.azurewebsites.net/get-a-token"  # Replace with your actual redirect URI.

    # msal_app = msal.ConfidentialClientApplication(client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. {CLIENT_ID}, {TENANT_ID}, {CLIENT_SECRET}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.function_name(name="GetAToken")
@app.route(route="get-a-token", auth_level=func.AuthLevel.ANONYMOUS)
def get_a_token(req: func.HttpRequest) -> func.HttpResponse:
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
    