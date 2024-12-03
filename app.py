from flask import Flask, request, jsonify

class FlaskWrapper:
  def __init__(self):
    self.app = Flask(__name__)
    #self.bot = Discord()
    self._setup_routes()

  def _setup_routes(self):
    @self.app.route('/')
    def index():
      return "Hello from FlaskWrapper!"

  def __call__(self, environ, start_response):
    return self.app.wsgi_app(environ, start_response)

  # def run_background_task(self):
  #   # Example background task.
  #   while True:
  #     print("Background task running...")
  #     import time
  #     time.sleep(5)

  def run(self):
    # Start background task in a separate thread.
    #hreading.Thread(target=self.run_background_task, daemon=True).start()
    # Run Flask in the main thread.
    self.app.run()

# Expose the WSGI-compatible object.
app = FlaskWrapper()

# app = Flask(__name__)

# @app.route('/')
# def index():
#   return "Hello World!"

# @app.route('/discord', methods=['GET', 'POST'])
# def discord():
#   if request.method == 'POST':
#     data = request.get_json()
#     if data and 'content' in data:
#       return jsonify({"content":data['content']})
#     else:
#       return jsonify({"error":"Missing 'content' in payload"}), 400
#   else:
#     return "Hello World!"
