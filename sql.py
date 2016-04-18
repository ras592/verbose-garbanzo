import sqlite3

def run_sql():
    with sqlite3.connect("sample.db") as connection:
        c = connection.cursor()
        create_test_table(c)
        create_basic_user_accts(c)
        create_global_modal_table(c)
        c.close()

def create_test_table(c):
    c.execute("""CREATE TABLE tests(title TEXT, description TEXT)""")
    c.execute('INSERT INTO tests VALUES("Test 1", "Hello, World!")')
    c.execute('INSERT INTO tests VALUES("Test 2", "Well, hi.")')

def create_basic_user_accts(c):
    c.execute("""CREATE TABLE users(username TEXT, password TEXT)""")
    c.execute('INSERT INTO users VALUES("admin", "admin")')
    c.commit()

def create_global_modal_table(c):
    c.execute("""
    CREATE TABLE MODEL(
        MODEL VARCHAR(20),
        PRICE DECIMAL(20, 2),
        TYPE VARCHAR(12),
        GAS_MILEAGE SMALLINT,
        SEAT SMALLINT,
        ENGINE DECIMAL(2,1)
        )
    """)
    c.execute("""
    INSERT INTO MODEL VALUES(
        "Tacoma",
        22000,
        "Truck",
        20,
        7,
        4.0
        )
    """)
    c.execute("""
    INSERT INTO MODEL VALUES(
        "Tundra",
        20000,
        "Truck",
        22,
        7,
        4.0
        )
    """)
    c.commit()
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

run_sql()
