from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/cpl')
def cpl():
    return render_template('cpl.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
