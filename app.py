from flask import Flask, render_template, session, url_for, flash, redirect, g, request, abort
from functools import wraps
from sql_schema import global_tables_tuple, stlouis_tables_tuple, kansascity_tables_tuple
import MySQLdb
import sql
import os

"""
Mediated Database Project:

WORKING:
1) Basic Routing
2) Login
3) Dynamic Global Display
4) Global Add Model POST

Changes made:
1) Added email field to all customers.
2) CHANGED DATE TO TRANS_DATE

TO-DO:
4) Adjust find_table to take a db name and perform searches on local dbs
5) Change things over to multiple users
6) Implement Insert for model and add_on
7) Select and return vehicles by price
8) Select and return vehicles by gas_mileage
9) Select and return vehicles by engine_size
# Write validate code
# Export Statement to SQL.py
# HOME: SHOULD BE CHANGED TO DASHBOARD FOR PERTINANT USER
"""

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or 'a hard to guess string'
app.current_dbs = list(sql.current_dbs)
app.mysql_host = os.environ.get('MYSQL_HOST') or "localhost"
app.mysql_user = os.environ.get('MYSQL_USER') or "rich"
app.mysql_passwd =  os.environ.get('MYSQL_PASSWD') or "some_pass"

# Opens MySQL connection
def connect_db():
    return MySQLdb.connect(host=app.mysql_host, user=app.mysql_user,
                            passwd=app.mysql_passwd)

def get_model_tables(db, models):
    model_tables = []
    try:
        for model in models:
            tables = []
            conn = connect_db()
            c = conn.cursor()
            query = 'SHOW COLUMNS FROM {0}.{1}'.format(db, model)
            c.execute(query)
            for row in c.fetchall():
                tables.append(row[0].lower())
            model_tables.append((model, tables))
            c.close()
    except Exception as e:
        print(e)
    return model_tables

# make the call to the database to initialize it
app.global_models = global_tables_tuple
app.global_model_tables = get_model_tables('global', app.global_models)
app.sl_models = stlouis_tables_tuple
app.sl_model_tables = get_model_tables('local_sl', app.sl_models)
app.kc_models = kansascity_tables_tuple
app.kc_model_tables = get_model_tables('local_kc', app.kc_models)

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

# SHOULD BE CHANGED TO DASHBOARD FOR PERTINANT USER
@app.route('/home')
@login_required
def home():
    errors = []
    cars=[]
    loggedin = loggedin_check()
    try:
        g.conn = connect_db() # g value is reset after each request
        res = sql.global_model_query(g.conn.cursor())
        for row in res: # fix for multiple users
            model=row[0]
            price=row[1]
            car_type=row[2]
            gas_mileage=row[3]
            seat=row[4]
            engine=row[5]
            cars.append(dict(model=model,price=price,type=car_type,gas_mileage=gas_mileage,seat=seat,engine=engine))
        g.conn.close()
    except Exception as e:
        print(e)
        g.conn.rollback()
        g.conn.close()
        flash('Database error!')
    return render_template('inventory.html', errors=errors, results=cars, loggedin=loggedin)

@app.route('/inventory')
def inventory():
    errors = []
    cars=[]
    loggedin = loggedin_check()
    try:
        g.conn = connect_db() # g value is reset after each request
        res = sql.global_model_query(g.conn.cursor())
        for row in res: # fix for multiple users
            model=row[0]
            price=row[1]
            car_type=row[2]
            gas_mileage=row[3]
            seat=row[4]
            engine=row[5]
            cars.append(dict(model=model,price=price,type=car_type,gas_mileage=gas_mileage,seat=seat,engine=engine))
        g.conn.close()
    except Exception as e:
        print(e)
        g.conn.rollback()
        g.conn.close()
        flash('Database error!')
    return render_template('inventory.html', errors=errors, results=cars, loggedin=loggedin)

@app.route('/add-model', methods=["GET", "POST"])
@login_required
def add_model():
    errors = []
    loggedin = loggedin_check()
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
                g.conn = connect_db() # g value is reset after each request
                sql.insert_global_model(g.conn, entry)
                flash('Your entry was recorded!')
                return redirect(url_for('inventory'))
            except Exception as e:
                print(e)
                g.conn.rollback()
                g.conn.close()
                flash('Database error!')
    return render_template('add_model.html', errors=errors, loggedin=loggedin)

@app.route('/add-add_on', methods=["GET", "POST"])
@login_required
def add_add_on():
    errors = []
    loggedin = loggedin_check()
    if request.method == 'POST':
        entry = dict(
            package_no=request.form['package_no'],
            package_description=request.form['package_description'],
            price=request.form['price'],
            model_available=request.form['model_available'],
            model=request.form['model']
        )
        errors += validate_dict(entry)
        if not errors:
            try:
                g.conn = connect_db() # g value is reset after each request
                sql.insert_global_add_on(g.conn, entry)
                flash('Your entry was recorded!')
                return redirect(url_for('inventory'))
            except Exception as e:
                print(e)
                g.conn.rollback()
                g.conn.close()
                flash('Database error!')
    return render_template('add_add_on.html', errors=errors, loggedin=loggedin)

@app.route('/add-rebate', methods=["GET", "POST"])
@login_required
def add_rebate():
    errors = []
    loggedin = loggedin_check()
    if 'dealer' in session:
        dealer = session['dealer']
    else:
        dealer = None
    if request.method == 'POST':
        entry = dict(
            model=request.form['model'],
            amount=request.form['amount'],
            start_date=request.form['start_time'],
            end_date=request.form['end_time']
        )
        errors += validate_dict(entry)
        if not errors:
            try:
                g.conn = connect_db() # g value is reset after each request
                if dealer == "local_sl":
                    sql.insert_local_sl_rebate(g.conn, entry)
                elif dealer == "local_kc":
                    sql.insert_local_kc_rebate(g.conn, entry)
                else:
                    abort(401)
                flash('Your rebate was recorded!')
                return redirect(url_for('home'))
            except Exception as e:
                print(e)
                g.conn.rollback()
                g.conn.close()
                flash('Database error!')
    return render_template('add_rebate.html', errors=errors, loggedin=loggedin)

@app.route('/stlouis/add-cars', methods=["GET", "POST"])
@login_required
def sl_add_cars():
    errors = []
    loggedin = loggedin_check()
    if request.method == 'POST':
        entry = dict(
            serialno=request.form['serialno'],
            model=request.form['model'],
            color=request.form['color'],
            autotrans=request.form['autotrans'],
            warehouse=request.form['warehouse']
        )
        errors += validate_dict(entry)
        if not errors:
            try:
                g.conn = connect_db() # g value is reset after each request
                sql.insert_local_sl_cars(g.conn, entry)
                flash('Your vehicle was recorded!')
                return redirect(url_for('home'))
            except Exception as e:
                print(e)
                g.conn.rollback()
                g.conn.close()
                flash('Database error!')
    return render_template('add_cars.html', errors=errors, loggedin=loggedin)

@app.route('/stlouis/cars')
def sl_cars():
    errors = []
    cars=[]
    loggedin = loggedin_check()
    try:
        g.conn = connect_db() # g value is reset after each request
        res = sql.select_local_sl_cars(g.conn.cursor())
        for row in res: # fix for multiple users
            serialno=row[0]
            model=row[1]
            color=row[2]
            autotrans=row[3]
            warehouse=row[4]
            cars.append(dict(serialno=serialno,model=model,color=color,autotrans=autotrans,warehouse=warehouse))
        g.conn.close()
    except Exception as e:
        print(e)
        g.conn.rollback()
        g.conn.close()
        flash('Database error!')
    return render_template('/views/sl_cars.html', errors=errors, results=cars, loggedin=loggedin)

@app.route('/kansascity/add-autos', methods=["GET", "POST"])
@login_required
def kc_add_autos():
    errors = []
    loggedin = loggedin_check()
    if request.method == 'POST':
        entry = dict(
            vehicle_no=request.form['vehicle_no'],
            model=request.form['model'],
            color=request.form['color'],
            autotrans=request.form['autotrans'],
            warehouse=request.form['warehouse'],
            financed=request.form['financed']
        )
        errors += validate_dict(entry)
        if not errors:
            try:
                g.conn = connect_db() # g value is reset after each request
                sql.insert_local_kc_autos(g.conn, entry)
                flash('Your vehicle was recorded!')
                return redirect(url_for('home'))
            except Exception as e:
                print(e)
                g.conn.rollback()
                g.conn.close()
                flash('Database error!')
    return render_template('add_autos.html', errors=errors, loggedin=loggedin)

@app.route('/kansascity/autos')
def kc_autos():
    errors = []
    cars=[]
    loggedin = loggedin_check()
    try:
        g.conn = connect_db() # g value is reset after each request
        res = sql.select_local_kc_autos(g.conn.cursor())
        for row in res: # fix for multiple users
            vehicle_no=row[0]
            model=row[1]
            color=row[2]
            autotrans=row[3]
            warehouse=row[4]
            financed=row[5]
            cars.append(dict(vehicle_no=vehicle_no,model=model,color=color,autotrans=autotrans,warehouse=warehouse,financed=financed))
        g.conn.close()
    except Exception as e:
        print(e)
        g.conn.rollback()
        g.conn.close()
        flash('Database error!')
    return render_template('/views/kc_autos.html', errors=errors, results=cars, loggedin=loggedin)

@app.route('/display/<model>')
@login_required
def display(model):
    print model
    template = 'views/'
    errors = []
    loggedin = loggedin_check()
    results = []
    if model.lower() in app.global_models:
        template = template + model.lower() + '.html'
        print template
        tables = app.global_model_tables
        query = 'select * from global.{0}'.format(model.lower())
        table = find_table(model.lower())
        try:
            g.conn = connect_db() # g value is reset after each request
            cur = g.conn.cursor()
            cur.execute(query)
            for row in cur.fetchall(): # fix for multiple users
                entry = {}
                i = 0
                for column in table:
                    entry[column] = row[i]
                    i+=1
                results.append(entry)
            g.conn.close()
        except Exception as e:
            print(e)
            g.conn.rollback()
            g.conn.close()
            flash('Database error!')
    else:
        abort(404)
    return render_template(template, errors=errors, results=results, loggedin=loggedin)

@app.route('/delete_user/<username>')
@login_required
def delete_user(username):
    try:
        g.conn = connect_db()
        sql.remove_user(g.conn, username)
        return redirect(url_for('display', model='users'))
    except Exception as e:
        print(e)
        g.conn.rollback()
        g.conn.close()
        flash('Database error!')
        return redirect(url_for('display', model='users'))

@app.route('/delete_cars/<serialno>')
@login_required
def delete_cars(serialno):
    try:
        g.conn = connect_db()
        sql.remove_cars(g.conn, serialno)
        return redirect(url_for('sl_cars'))
    except Exception as e:
        print(e)
        g.conn.rollback()
        g.conn.close()
        flash('Database error!')
        return redirect(url_for('sl_cars'))

@app.route('/delete_autos/<vehicle_no>')
@login_required
def delete_autos(vehicle_no):
    try:
        g.conn = connect_db()
        sql.remove_autos(g.conn, vehicle_no)
        return redirect(url_for('kc_autos'))
    except Exception as e:
        print(e)
        g.conn.rollback()
        g.conn.close()
        flash('Database error!')
        return redirect(url_for('kc_autos'))

@app.route('/login', methods=["GET", "POST"])
def login():
    errors = []
    if request.method == 'POST':
        username, password = None, None
        try:
            username = validate(request.form['username'])
            password = validate(request.form['password'])

            g.conn = connect_db() # g value is reset after each request
            res = sql.global_user_authenticate(g.conn, [username, password])
            if res is not None:
                username=res[0]
                g.conn.close()
                session['logged-in'] = True
                session['username'] = username
                session['dealer'] = "local_sl" # change for different users their location
                flash('You were just logged in!')
                return redirect(url_for('home'))
            else:
                errors.append('Incorrect login information')
        except Exception as e:
            print(e)
            g.conn.rollback()
            g.conn.close()
            flash('Database error!')
    return render_template('login.html', errors=errors, loggedin=False)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged-in', None)
    flash('You were just logged out!')
    return redirect(url_for('index'))

@app.errorhandler(401)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 401 # Return a particular template

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Validates user is logged in
def loggedin_check():
    loggedin=False
    if 'logged-in' in session:
        loggedin=session['logged-in']
    return loggedin

# Checks for table in tuple and returns a list of column names
# Adjust find_table to take a db name and perform searches on local dbs
def find_table(model):
    for tup in app.global_model_tables:
        if tup[0] == model:
            return tup[1]

# Use validate_dict for POSTing new values into DB
def validate_dict(dict_obj):
    errors = []
    for k,v in dict_obj.items():
        if not v:
            errors.append("{0} has no value".format(k))
    return errors

# Escapes and validates user input for sql statements
# Write validate code
def validate(user_input):
    return user_input

def async_cron_job(app):
    with app.app_context():
        sql.remove_old_rebates(connect_db())

def cron_job():
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

if __name__ == '__main__':
    app.run(debug=True)
