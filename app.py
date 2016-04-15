from flask import Flask, render_template, session, url_for, flash, redirect, g, request
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = 'a hard to guess string'
app.database = 'sample.db'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged-in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    errors = None
    return render_template('index.html', errors=errors)

@app.route('/home')
@login_required
def home():
    errors = None
    username = 'admin'
    try:
        g.db = connect_db() # g value is reset after each request
        cur = g.db.execute('select * from tests')
        tests = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
        g.db.close()
    except sqlite3.OperationalError:
        flash('You have no database!')
    return render_template('home.html', username=username, tests=tests)

@app.route('/login', methods=["GET", "POST"])
def login():
    errors = None
    if request.method == 'POST':
        username, password = None, None
        try:
            g.db = connect_db() # g value is reset after each request
            cur = g.db.execute('select * from users')
            for row in cur.fetchall():
                username=row[0]
                password=row[1]
            g.db.close()

            if request.form['username'] == username and request.form['password'] == password:
                session['logged-in'] = True
                flash('You were just logged in!')
                return redirect(url_for('home'))
            else:
                errors = 'Incorrect login information'
        except sqlite3.OperationalError:
            flash('You have no database!')
    return render_template('login.html', errors=errors)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged-in', None)
    flash('You were just logged out!')
    return redirect(url_for('index'))

def connect_db():
    return sqlite3.connect(app.database)

if __name__ == '__main__':
    app.run(debug=True)
