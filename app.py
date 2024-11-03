from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    client_id = os.getenv('CLIENT_ID')
    return render_template('index.html', client=client_id)
    
@app.route('/cpl')
def control_panel():
    return render_template('control_panel.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
