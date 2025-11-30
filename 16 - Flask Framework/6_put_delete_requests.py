from flask import *
import sqlite3 as sql
import json
import random

app = Flask(__name__, template_folder = "project_templates")
app.secret_key = str(random.randint(10000000000000000000000000, 99999999999999999999999999))

def getdb():
    database = sql.connect('6_lists.db')
    cursor = database.cursor()
    return (database, cursor)

(database, cursor) = getdb()
cursor.execute('''
    create table if not exists lists(
        username text primary key,
        password text,
        list_items text
    )
''')
database.commit()
database.close()

def execute_find_query(username):
    (database, cursor) = getdb()
    query = f'''
        select * from lists
        where username = '{username}'
    '''
    record = cursor.execute(query).fetchone()
    database.close()
    return record

def execute_insert_query(username, password):
    (database, cursor) = getdb()
    query = f'''
        insert into lists values
        ('{username}','{password}','')
    '''
    cursor.execute(query)
    database.commit()
    database.close()

def execute_update_query(username, newlist):
    (database, cursor) = getdb()
    query = f'''
        update lists
        set list_items = '{newlist}'
        where username = '{username}'
    '''
    cursor.execute(query)
    database.commit()
    database.close()

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('signup_login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        record = execute_find_query(username)

        if record:
            stored_pass = record[1]

            if password == stored_pass:
                session['user_id'] = username
                return render_template('to_do_list.html', username = username, message = f"Welcome back {username}, You know what to do !", tasks = json.loads(record[2]) if len(record[2]) else {})
            else:
                return "Wrong Password"
        else:
            execute_insert_query(username, password)
            session['user_id'] = username
            return render_template('to_do_list.html', username = username, message = f"Welcome {username}, Add tasks using + and remove using - !", tasks = {})

@app.route('/list', methods = ['POST'])
def list_operations():
    if 'user_id' not in session:        # invalid user
        return redirect('/')
    
    username = session['user_id']
    record = execute_find_query(username)
    
    if request.form['action'] == 'add':
        old_tasks = json.loads(record[2]) if len(record[2]) else dict()
        new_task = request.form['new_task']

        if len(new_task):
            old_tasks[len(old_tasks)] = new_task
            new_tasks = json.dumps(old_tasks)
            execute_update_query(username, new_tasks)

        return render_template('to_do_list.html', username = username, message = f"Added {new_task if len(new_task) else "none"}", tasks = old_tasks)
    
    elif request.form['action'] == 'remove':
        old_tasks = json.loads(record[2]) if len(record[2]) else dict()
        new_tasks = dict()
        removed = []
        i = 0
        for task in old_tasks.values():
            if task in request.form:
                removed.append(task)
                continue
            else:
                new_tasks[i] = task
                i += 1

        removed_tasks = json.dumps(new_tasks)
        execute_update_query(username, removed_tasks)

        additional_msg = ""
        if len(removed) == 0: additional_msg = "none"
        elif len(removed) == 1: additional_msg = removed[0]
        else: additional_msg = "multiple items"

        return render_template('to_do_list.html', username = username, message = f"Removed {additional_msg}", tasks = new_tasks)


if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)