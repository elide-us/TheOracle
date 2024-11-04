from flask import Flask, render_template
import os
import msal

CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html', client=CLIENT_ID, tenant=TENANT_ID, secret=CLIENT_SECRET)

@app.route('/redirect')
def redirect():
    return render_template('redirect.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
