import MySQLdb
from sql_schema import global_insert_data, global_tables, \
                        stlouis_tables, kansascity_tables, global_tables_tuple,\
                        stlouis_tables_tuple, kansascity_tables_tuple

"""
sql.py
All of the methods to operate on the databases.
References model statements in sql_schema.py

TO-DO:
1) Phone number strip all nonnumeric chars
2) Validate emails

"""

current_dbs = ["global", "local_sl", "local_kc"]

"""
CREATE Databases
"""
def create_mysql_db(cursor, dbs):
    try:
        for db in dbs:
            cursor.execute("CREATE DATABASE IF NOT EXISTS " + db)
    except Exception as e:
        raise

"""
DROP Databases
"""
def drop_mysql_db(cursor, dbs):
    drop_dbs = list(dbs)
    if ('local_kc' in dbs or 'local_sl' in dbs) and 'global' in dbs:
        index = drop_dbs.index('global')
        drop_dbs.pop(index)
        try:
            for db in drop_dbs:
                cursor.execute("DROP DATABASE IF EXISTS " + db)
            cursor.execute("DROP DATABASE IF EXISTS global")
        except Exception as e:
            raise
    else:
        try:
            for db in dbs:
                cursor.execute("DROP DATABASE " + db)
        except Exception as e:
            raise

"""
Creates all dbs
Default is all current databases in current_dbs array
"""
def build_dbs(conn, dbs=current_dbs):
    try:
        create_mysql_db(conn.cursor(), dbs)
        rebuild_tables(conn, ['global', 'local_sl', 'local_kc'])
    except Exception as e:
        raise

"""
Removes all dbs
Default is all current databases in current_dbs array
"""
def destroy_dbs(conn, dbs=current_dbs):
    try:
        drop_mysql_db(conn.cursor(), dbs)
    except Exception as e:
        raise

"""
Inserts tables for all dbs
Pass array
"""
def rebuild_tables(conn, dbs=current_dbs):
    tables_titles = ()
    tables = {}
    try:
        cursor = conn.cursor()
        for db in dbs:
            if db is current_dbs[0]:
                table_titles = global_tables_tuple
                tables = global_tables
            elif db is current_dbs[1]:
                table_titles = stlouis_tables_tuple
                tables = stlouis_tables
            elif db is current_dbs[2]:
                table_titles = kansascity_tables_tuple
                tables = kansascity_tables
            else:
                table_titles = ()
                tables = {}
            for k in table_titles:
                print tables[k]
                cursor.execute(tables[k])
    except Exception as e:
        raise

# Insert Global Model
def insert_global_model(conn, values):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO global.model VALUES("{0}",{1}, "{2}", {3}, {4}, {5})'.format(
            values['model'], values['price'], values['car_type'], values['gas_mileage'], values['seat'], values['engine']
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        raise

# Basic global model query
def global_model_query(cursor):
    try:
        query = 'SELECT * FROM global.model'
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise

# Insert Local_sl Rebate
def insert_local_sl_rebate(conn, values):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO local_sl.rebate1 VALUES("{0}",{1}, "{2}", "{3}")'.format(
            values['model'], values['amount'], values['start_date'], values['end_date']
        ))
        conn.commit()
        # insert global
        values['dealer'] = 'local_sl'
        insert_global_rebate(conn, values)
        conn.close()
    except Exception as e:
        raise

# SELECT local_sl rebate
def select_local_sl_rebate(cursor):
    try:
        query = 'SELECT * FROM local_sl.rebate1'
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise

# Insert Local_kc Rebate
def insert_local_kc_rebate(conn, values):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO local_kc.rebate2 VALUES("{0}",{1}, "{2}", "{3}")'.format(
            values['model'], values['amount'], values['start_date'], values['end_date']
        ))
        conn.commit()
        # insert global
        values['dealer'] = 'local_kc'
        insert_global_rebate(conn, values)
        conn.close()
    except Exception as e:
        raise

# SELECT local_kc rebate
def select_local_kc_rebate(cursor):
    try:
        query = 'SELECT * FROM local_kc.rebate2'
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise

# Insert global Rebate
def insert_global_rebate(conn, values):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO global.rebate_global VALUES("{0}",{1}, "{2}", "{3}", "{4}")'.format(
            values['model'], values['amount'], values['dealer'], values['start_date'], values['end_date']
        ))
        conn.commit()
    except Exception as e:
        raise

# SELECT global rebate
def select_global_rebate(cursor):
    try:
        query = 'SELECT * FROM global.rebate_global'
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise

def remove_old_rebates(conn):
    try:
        c = conn.cursor()
        query = 'DELETE FROM global.rebate_global WHERE end_date< NOW()'
        c.execute(query)
        conn.commit()
        query = 'DELETE FROM local_sl.rebate1 WHERE end_date< NOW()'
        c.execute(query)
        conn.commit()
        query = 'DELETE FROM local_kc.rebate2 WHERE end_date< NOW()'
        c.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        raise


# username password authentication query
def global_user_authenticate(conn, values):
    try:
        c = conn.cursor()
        query = """
        SELECT * FROM global.users WHERE username = '{0}' AND password = SHA('{1}')
        """.format(values[0], values[1])
        c.execute(query)
        return c.fetchone()
    except Exception as e:
        raise

################################################################

# Insert All Fake Table Data
# Should take array of each dbs tables

# Insert Fake Table Data
# Should take a table key

def insert_global_user_data(c):
    for s in global_insert_data['insert_global_users']:
        c.execute(s)

def insert_global_model_data(c):
    for s in global_insert_data['insert_global_model']:
        c.execute(s)
