from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Index route to render the button and message
@app.route('/')
def index():
    return render_template('index.html')

# MSAL redirect route placeholder
@app.route('/auth/redirect')
def msal_redirect():
    # Placeholder logic for handling MSAL token return
    return "MSAL redirect handled here"

if __name__ == '__main__':
    app.run(debug=True)
