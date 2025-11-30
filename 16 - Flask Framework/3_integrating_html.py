from flask import Flask
from flask import render_template   # function used to redirect http requests using html templates
# all templates must be defined inside templates folder at same hierarchy as app.py

app = Flask(__name__)

# manually returning html
@app.route('/')
def welcome():
    return '''
    <html>
        <head>
            <title>Flask Apps</title>
        </head>
        <body>
            <h1> This is My First Flask App</h1>
            <h2>This is returned manually</h2>
            <a href = "/index"> Index </a>
            <a href = "/about"> About Us </a>
        </body>
    </html>
    '''
# returning a template using render_template() function
@app.route('/index')
def render_index():
    return render_template('index.html')        # must be inside "templates" folder

@app.route('/about')
def render_about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port =  8080, debug = True)