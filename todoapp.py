from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
import re
import sys
import sqlite3

app = Flask(__name__, template_folder='templates')
con = sqlite3.connect('todo.db', check_same_thread=False)
cur = con.cursor()
create_table = "CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, activity TEXT, email TEXT, priority text)"

cur.executescript(create_table)
con.commit()



def loadTask(activity, email, priority):
    insert = f"insert into todo (activity, email, priority) values('{activity}', '{email}', '{priority}')"
    cur.executescript(insert)
    con.commit()

def getData():
    initial = [
    ("Meditate", "a@gmail.com", "High"),
    ("Execise", "blink@yahoo.com", "High"),
    ("Do Homework", "hw@aol.com", "High"),
]
    get_data = "Select * from todo"
    cur.execute(get_data)
    con.commit()
    rows = cur.fetchall()
    if len(rows) < 1:
        for task in initial:
            loadTask(task[0], task[1], task[2])
        get_data = "Select * from todo"
        cur.execute(get_data)
        con.commit()
        rows = cur.fetchall()
    
    return rows

def deleteTask(id):
    delete = f"delete from todo where id ={id}"
    cur.executescript(delete)
    con.commit()

def deleteAll():
    delete = f"delete from todo"
    cur.executescript(delete)
    con.commit()

def check(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, email)):
        return True
 
    else:
        return False

todo_list = getData()
print(todo_list)
@app.route('/')
def display_list():
    return render_template('todo.html', todo_list=todo_list)


@app.route('/submit', methods=["POST"])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']
    if check(email) is True:
        loadTask(task, email, priority)
        todo_list = getData()
        return redirect(url_for('display_list'))
    else:
        error = 'Invalid credentials'
        return render_template('todo.html', todo_list=todo_list, error=error)

@app.route('/remove', methods=["post"])
def remove():
    deleteTask(request.args["id"])
    todo_list =  getData()
    print(todo_list)
    return render_template('todo.html', todo_list=todo_list)



@app.route('/clear')
def clear():
    global todo_list
    todo_list = []
    deleteAll()
    return redirect(url_for('display_list'))


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)