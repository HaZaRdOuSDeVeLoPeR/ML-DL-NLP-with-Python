from flask import *

app = Flask(__name__)

#         specifying which http request methods are allowed in this route
@app.route('/', methods = ['GET'])      
def homepage():
    return render_template('homepage.html')

# multiple types of http requests allowed at same route
@app.route('/info', methods=['GET', 'POST'])
def info_page():
    if request.method == 'GET':             # serve if GET request
        return render_template('info.html')

    elif request.method == 'POST':          # serve if post request
        form_data = request.form
        print("Form Data Retrived: ", form_data)
        return f"Hello {form_data['name']}"

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)