from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "secret"

# CREATE DATABASE

def init_db():

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee TEXT,
            task TEXT,
            deadline TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# LOGIN

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':

            session['logged_in'] = True

            return redirect('/dashboard')

        else:

            return "Invalid Login"

    return render_template('login.html')

# DASHBOARD

@app.route('/dashboard')
def dashboard():

    if not session.get('logged_in'):
        return redirect('/')

    conn = sqlite3.connect('employee.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")

    tasks = cur.fetchall()

    conn.close()

    return render_template('dashboard.html', tasks=tasks)

# ADD TASK

@app.route('/add', methods=['GET', 'POST'])
def add_task():

    if not session.get('logged_in'):
        return redirect('/')

    if request.method == 'POST':

        employee = request.form['employee']
        task = request.form['task']
        deadline = request.form['deadline']
        status = request.form['status']

        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO tasks(employee, task, deadline, status) VALUES (?, ?, ?, ?)",
            (employee, task, deadline, status)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_task.html')

# LOGOUT

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# RUN

if __name__ == '__main__':
    app.run(debug=True)