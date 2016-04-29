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

################################################################
################################################################
################################################################
################################################################

# Insert Data

def insert_global_model(c, values):
    try:
        c.execute('INSERT INTO MODEL VALUES("{0}",{1}, "{2}", {3}, {4}, {5})'.format(
            values['model'], values['price'], values['car_type'], values['gas_mileage'], values['seat'], values['engine']
        ))
        c.commit()
        c.close()
    except Exception as e:
        raise

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

"""
Global Views
==========================
---------------------------
Table: MODEL
PK: MODEL (ex: Tacoma, Tundra) VARCHAR/TEXT
PRICE (ex: $22,000.00) Float/Decimal/Money
TYPE (ex: Truck, Sedan, SUV) VARCHAR/TEXT
GAS_MILEAGE (ex: 20, 25, 30) smallint
SEAT (ex: 7, 5, 4) tinyint
ENGINE (ex: 4.0, 5.6, 3.5) Float/Decimal
---------------------------
Table: ADD_ON
PK: PACKAGE_NO (ex:)
PACKAGE_DESCRIPTION (ex:)
PRICE (ex:)
MODEL_AVAILABLE (ex:)
---------------------------
Table: POTENTIAL_BUYER
PK: BUYER_NO (ex:)
NAME (ex:)
ADDRESS (ex:)
PHONE (ex:)
EMAIL (ex:)
---------------------------
Table: AVAILABLE_AUTO
PK: SERIAL_NO (ex:)
MODEL (ex:)
COLOR (ex:)
DEALER (ex:)
---------------------------
Table: SALESPERSON
PK: REP_NO (ex:)
BASE_SALARY (ex:)
YTD_SALES (ex:)
COMM (ex:)
---------------------------
Table: CUSTOMER_GLOBAL
PK: CUSTOMER_NO (ex:)
NAME (ex:)
ADDRESS (ex:)
PHONE (ex:)
---------------------------
Table: EMPLOYEE
PK: EMP_NO (ex:)
NAME (ex:)
ADDRESS (ex:)
PHONE (ex:)
POSITION (ex:)
---------------------------
Table: SALES
PK: TRANSACTION_NO (ex:)
REP_NO (ex:)
CUSTOMER_NO (ex:)
VEH_NO (ex:)
DATE (ex:)
---------------------------
Table: REBATE_GLOBAL
PK: MODEL (ex:)
AMOUNT (ex:)
DEALER (ex:)
START_DATE (ex:)
END_DATE (ex:)
---------------------------
"""

"""
Local Views - Dealer One
==========================
---------------------------
Table: CARS
PK: SERIALNO (ex:)
MODEL (ex:)
COLOR (ex:)
AUTOTRANS (ex:)
WAREHOUSE (ex:)
---------------------------
Table: REPRESENTATIVE
PK: REP_NO (ex:)
NAME (ex:)
ADDRESS (ex:)
PHONE (ex:)
BASE_SALARY (ex:)
YTD_SALES (ex:)
COMM (ex:)
---------------------------
Table: CUSTOMER_D1
PK: CUSTOMER_NO (ex:)
NAME (ex:)
ADDRESS (ex:)
PHONE (ex:)
---------------------------
Table: LOAN
PK: SERIAL_NO (ex:)
AMOUNT (ex:)
START_DATE (ex:)
END_DATE (ex:)
---------------------------
Table: REBATE1
PK: MODEL (ex:)
AMOUNT (ex:)
START_DATE (ex:)
END_DATE (ex:)
---------------------------
Table: TRANSACTION
PK: DEAL_NO (ex:)
REP_NO (ex:)
CUSTOMER_NO (ex:)
SERIAL_NO (ex:)
AMOUNT (ex:)
FIN_AMT (ex:)
DATE (ex:)
REBATE_AMT (ex:)
---------------------------
"""

"""
Local Views - Dealer Two
==========================
---------------------------
Table: CARS
PK: VEHICLE_NO (ex:)
MODEL (ex:)
COLOR (ex:)
AUTOTRANS (ex:)
WAREHOUSE (ex:)
FINANCED (ex:)
---------------------------
Table: SALES_PERSON
PK: SALE_NO (ex:)
NAME (ex:)
ADDRESS (ex:)
PHONE (ex:)
COMM (ex:)
BASE_SALARY (ex:)
YTDSALES (ex:)
---------------------------
Table: CUSTOMER_D2
PK: BUYER_NO (ex:)
NAME (ex:)
ADDRESS (ex:)
PHONE (ex:)
---------------------------
Table: FINANCE
PK: VEHICLE_NO (ex:)
BUYER_NO (ex:)
AMOUNT (ex:)
MONTHS (ex:)
BALANCE (ex:)
---------------------------
Table: REBATE2
PK: MODEL (ex:)
AMOUNT (ex:)
START_DATE (ex:)
END_DATE (ex:)
---------------------------
Table: DEAL
PK: DEAL_NO (ex:)
REP_NO (ex:)
CUSTOMER_NO (ex:)
SERIAL_NO (ex:)
AMOUNT (ex:)
FIN_AMT (ex:)
DATE (ex:)
REBATE_AMT (ex:)
---------------------------
"""
