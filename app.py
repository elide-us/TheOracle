from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello World!"

@app.route('/discord', methods=['GET', 'POST'])
def discord():
  if request.method == 'POST':
    data = request.get_json()
    if data and 'content' in data:
      return jsonify({"content":data['content']})
    else:
      return jsonify({"error":"Missing 'content' in payload"}), 400
  else:
    return "Hello World!"

# Remember, `app` will be called directly from gunicorn as `app:app`
