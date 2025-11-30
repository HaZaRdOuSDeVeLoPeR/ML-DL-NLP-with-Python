# must install flask module
from flask import Flask         # import Flask class from flask package

# Syntax :- app = Flask(module)     Here module defines the scope of flask app (modules which belongs to the flask app)
app = Flask(__name__)           # create an instance of Flask App (WSGI App)

@app.route('/')                 # serve get requests on home route
def welcome():                  # view function
    return "<h1>Welcome to First Flask App</h1>"

# when a file is run directly, __name__ = __main___
# when a file is imported into another file, then __name__ = __file_name__ for the file which is imported

# this ensures the block runs only when it is run directly and not when it is imported
if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)
    # host : ip address of server
    # port : port on web server
    # debug : when true, goes into development mode (restarts server if code is updated)