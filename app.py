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

@app.route('/inventory')
@login_required
def inventory():
    errors = None
    cars=[]
    try:
        g.db = connect_db() # g value is reset after each request
        cur = g.db.execute('select * from MODEL')
        for row in cur.fetchall(): # fix for multiple users
            model=row[0]
            price=row[1]
            car_type=row[2]
            gas_mileage=row[3]
            seat=row[4]
            engine=row[5]
            cars.append(dict(model=model,price=price,car_type=car_type,gas_mileage=gas_mileage,seat=seat,engine=engine))
        g.db.close()
    except sqlite3.OperationalError:
        flash('You have no database!')
    return render_template('inventory.html', results=cars)

@app.route('/add-model', methods=["GET", "POST"])
#@login_required
def add_model():
    errors = []
    if request.method == 'POST':
        entry = dict(
            model=request.form['model_model'],
            price=request.form['model_price'],
            car_type=request.form['model_car_type'],
            gas_mileage=request.form['model_gas_mileage'],
            seat=request.form['model_seat'],
            engine=request.form['model_engine']
        )
        for k,v in entry.items():
            if not v:
                errors.append("{0} has no value".format(k))
        if not errors:
            try:
                g.db = connect_db() # g value is reset after each request
                query = 'INSERT INTO MODEL VALUES("{0}",{1}, "{2}", {3}, {4}, {5})'.format(
                    entry['model'], entry['price'], entry['car_type'], entry['gas_mileage'], entry['seat'], entry['engine']
                )
                g.db.execute(query)
                g.db.commit()
                g.db.close()
                flash('Your entry was recorded!')
                return redirect(url_for('inventory'))
            except sqlite3.OperationalError:
                flash('You have no database!')

    return render_template('add_model.html', errors=errors)


@app.route('/login', methods=["GET", "POST"])
def login():
    errors = None
    if request.method == 'POST':
        username, password = None, None
        try:
            g.db = connect_db() # g value is reset after each request
            cur = g.db.execute('select * from users')
            for row in cur.fetchall(): # fix for multiple users
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
