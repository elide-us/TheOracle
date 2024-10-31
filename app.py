from flask import Flask, render_template

# Create the Flask application instance
app = Flask(__name__)

# Define a route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Hello World</title>
#   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
# </head>
# <body>
#   <div class="container">
#     <div class="row">
#         <div class="col-md-12 text-center">
#           <div class="card mt-5" style="display: inline-block;">
#             <div class="card-body">
#               <h1 class="display-4 text-primary">Hello World</h1>
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
# </body>
# </html>
