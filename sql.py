import sqlite3
from sql_schema import global_insert_data, global_tables

"""
TO-DO:
1) Phone number strip all nonnumeric chars
2) Validate emails

"""

# Builds DBs
def run_sql():
    # I should check if the db exists if so delete it
    with sqlite3.connect("global.db") as connection:
        c = connection.cursor()
        create_global_user_table(c)
        create_global_model_table(c)
        create_global_add_on_table(c)
        rebuild(c)
        c.close()

# Used to insert old data back into db
def rebuild(c):
    insert_global_model_data(c)
    insert_global_user_data(c)

# Create Tables

def create_global_user_table(c):
    c.execute(global_tables['users'])

def create_global_model_table(c):
    c.execute(global_tables['MODEL'])

def create_global_add_on_table(c):
    c.execute(global_tables['ADD_ON'])

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

# Insert Fake Table Data

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
