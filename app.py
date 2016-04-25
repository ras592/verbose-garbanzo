from flask import Flask, render_template, session, url_for, flash, redirect, g, request
from functools import wraps
import sqlite3
import sql

app = Flask(__name__)

app.secret_key = 'a hard to guess string'
app.database = 'global.db'

def get_global_models(db):
    global_models = []
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        res = c.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        for row in res.fetchall():
            global_models.append(row[0].lower())
        c.close()
    except Exception as e:
        print(e)
    return global_models

def get_global_models_tables(db):
    global_models_tables = []
    try:
        for model in app.global_models:
            tables = []
            conn = sqlite3.connect(db)
            c = conn.cursor()
            query = 'PRAGMA table_info({})'.format(model)
            res = c.execute(query)
            for row in res.fetchall():
                tables.append(row[1].lower())
            global_models_tables.append((model, tables))
            c.close()
    except Exception as e:
        print(e)
    return global_models_tables

# make the call to the database to initialize it
app.global_models = get_global_models(app.database) # change to global db
app.global_models_tables = get_global_models_tables(app.database) # change to global db

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
    errors = []
    loggedin = loggedin_check()
    return render_template('index.html', errors=errors, loggedin=loggedin)

@app.route('/home')
@login_required
def home():
    errors = []
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
            cars.append(dict(model=model,price=price,type=car_type,gas_mileage=gas_mileage,seat=seat,engine=engine))
        g.db.close()
    except Exception as e:
        print(e)
        g.db.rollback()
        g.db.close()
        flash('Database error!')
    return render_template('inventory.html', errors=errors, results=cars, loggedin=session['logged-in'])

@app.route('/inventory')
def inventory():
    errors = []
    cars=[]
    loggedin = loggedin_check()
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
            cars.append(dict(model=model,price=price,type=car_type,gas_mileage=gas_mileage,seat=seat,engine=engine))
        g.db.close()
    except Exception as e:
        print(e)
        g.db.rollback()
        g.db.close()
        flash('Database error!')
    return render_template('inventory.html', errors=errors, results=cars, loggedin=loggedin)

@app.route('/add-model', methods=["GET", "POST"])
@login_required
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
        errors += validate_dict(entry)
        if not errors:
            try:
                g.db = connect_db() # g value is reset after each request
                sql.insert_global_model(g.db, entry)
                flash('Your entry was recorded!')
                return redirect(url_for('inventory'))
            except Exception as e:
                print(e)
                g.db.rollback()
                g.db.close()
                flash('Database error!')
    return render_template('add_model.html', errors=errors, loggedin=session['logged-in'])

@app.route('/display/<model>')
@login_required
def display(model):
    template = 'views/'
    errors = []
    loggedin = loggedin_check()
    results = []
    if model.lower() in app.global_models:
        template = template + model.lower() + '.html'
        tables = app.global_models_tables
        query = 'select * from {0}'.format(model.lower())
        table = find_table(model.lower())
        try:
            g.db = connect_db() # g value is reset after each request
            cur = g.db.execute(query)
            for row in cur.fetchall(): # fix for multiple users
                entry = {}
                i = 0
                for column in table:
                    entry[column] = row[i]
                    i+=1
                results.append(entry)
            g.db.close()
        except Exception as e:
            print(e)
            g.db.rollback()
            g.db.close()
            flash('Database error!')
    else:
        errors.append("{} does not exist".format(model))
        template = '404.html' # make 404 with descriptive fix
    return render_template(template, errors=errors, results=results, loggedin=loggedin)

@app.route('/login', methods=["GET", "POST"])
def login():
    errors = []
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
                session['username'] = username
                flash('You were just logged in!')
                return redirect(url_for('home'))
            else:
                errors = 'Incorrect login information'
        except Exception as e:
            print(e)
            g.db.rollback()
            g.db.close()
            flash('Database error!')
    return render_template('login.html', errors=errors, loggedin=False)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged-in', None)
    flash('You were just logged out!')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

def connect_db():
    return sqlite3.connect(app.database)

def loggedin_check():
    loggedin=False
    if 'logged-in' in session:
        loggedin=session['logged-in']
    return loggedin

def find_table(model):
    for tup in app.global_models_tables:
        if tup[0] == model:
            return tup[1]

def validate_dict(dict_obj):
    errors = []
    for k,v in dict_obj.items():
        if not v:
            errors.append("{0} has no value".format(k))
    return errors

if __name__ == '__main__':
    app.run(debug=True)
