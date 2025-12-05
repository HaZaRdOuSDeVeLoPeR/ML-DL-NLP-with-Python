from flask import *
import sqlite3 as sql

app = Flask(__name__, template_folder = 'dynamic_templates')
database = sql.connect('5_marks.db')
cursor = database.cursor()

# make table if not exits
make_table_query = '''
    create table if not exists marks(
        roll_no text Primary Key,
        name text,
        english Integer,
        hindi Integer,
        maths Integer,
        science Integer
    )
'''
cursor.execute(make_table_query)
database.commit()
database.close()

# add a entry 
def add_entry(roll, name, eng, hin, maths, sci):
    add_query = f'''
        insert into marks values
        ('{roll}', '{name}', {eng}, {hin}, {maths}, {sci})
    '''
    database = sql.connect('5_marks.db')
    cursor = database.cursor()
    cursor.execute(add_query)
    database.commit()               # must commit and close
    database.close()

# get a entry for (name, roll)
def fetch_entry(roll, name):
    database = sql.connect('5_marks.db')
    cursor = database.cursor()
    cursor.execute(f'''
        select * from marks
        where roll_no = "{roll}" and name = "{name}"
    ''')
    records = cursor.fetchall()
    database.close()
    return records

# welcome the use on homeroute
@app.route('/')
def welcome():
    return render_template('welcome.html')

# serve get request on get marks form
@app.route('/getform', methods=['GET'])
def know_marks():
    return render_template('getform.html')

######################## building url dynamically ######################
# serve get request on get marks form (variable url)
@app.route('/getmarks', methods = ['GET'])
def display_marks():
    name = request.args['name']     # extract the values of arguments from url
    roll = request.args['roll']
    entry = fetch_entry(roll, name)
    if len(entry):
        entry = entry[0]
        return render_template('marks_info.html', data = entry)
    else:
        return render_template('done.html', title = "Error", msg = "No Records Found")

########################### variable arguments ##########################
# predefined syntax for variable url
@app.route('/getmarks/<name>/<roll>', methods = ['GET'])
def display_marks_manually(roll, name):     # access the parameter inside function
    entry = fetch_entry(roll, name)
    if len(entry):
        entry = entry[0]
        return render_template('marks_info.html', data = entry)
    else:
        return render_template('done.html', title = "Error", msg = "No Records Found")

# serve get/post request on post marks form
@app.route('/postform', methods=['GET', 'POST'])
def submit_marks():
    if(request.method == "GET"):
        return render_template('postform.html')
    else:
        form_data = request.form
        print(form_data)
        add_entry(form_data['roll'], form_data['name'], form_data['english'], form_data['hindi'], form_data['maths'], form_data['science'])
        return render_template('done.html', title = "Success", msg = "Successfully Submitted")
        
# start the app
if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)