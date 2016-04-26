"""
CREATE Global Tables
"""
global_tables = {
    "MODEL": """
    CREATE TABLE MODEL(
        MODEL VARCHAR(45) PRIMARY KEY,
        PRICE NOT NULL DECIMAL(20, 2),
        TYPE NOT NULL VARCHAR(45),
        GAS_MILEAGE NOT NULL SMALLINT,
        SEAT NOT NULL SMALLINT,
        ENGINE NOT NULL DECIMAL(2,1),
        CONSTRAINT model_unique UNIQUE (MODEL)
        )
    """,
    "users": """CREATE TABLE users(username TEXT, password TEXT)""",
    "ADD_ON": """
    CREATE TABLE ADD_ON(
        PACKAGE_NO VARCHAR(4) PRIMARY KEY,
        PACKAGE_DESCRIPTION NOT NULL VARCHAR(45),
        PRICE NOT NULL DECIMAL(20, 2),
        MODEL_AVAILABLE NOT NULL VARCHAR(45),
        MODEL NOT NULL VARCHAR(45),
        FOREIGN KEY (MODEL) REFERENCES MODEL(MODEL),
        CONSTRAINT package_no_unique UNIQUE (PACKAGE_NO)
        )
    """,
    "EMPLOYEE": """
    CREATE TABLE EMPLOYEE(
        EMP_NO INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME NOT NULL VARCHAR(45),
        ADDRESS NOT NULL VARCHAR(45),
        PHONE NOT NULL CHAR(10),
        POSITION NOT NULL VARCHAR(45)
        CONSTRAINT emp_no_unique UNIQUE (EMP_NO)
        )
    """,
    "SALESPERSON": """
    CREATE TABLE SALESPERSON(
        REP_NO INTEGER PRIMARY KEY,
        BASE_SALARY NOT NULL DECIMAL(20, 2) DEFAULT 0,
        YTD_SALES NOT NULL DECIMAL(20, 2) DEFAULT 0,
        COMM NOT NULL DECIMAL(20, 2) DEFAULT 0,
        FOREIGN KEY (REP_NO) REFERENCES EMPLOYEE(EMP_NO),
        CONSTRAINT rep_no_unique UNIQUE (REP_NO)
    )
    """,
    "POTENTIAL_BUYER": """
    CREATE TABLE POTENTIAL_BUYER(
        BUYER_NO INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME NOT NULL VARCHAR(45),
        ADDRESS NOT NULL VARCHAR(45),
        PHONE NOT NULL CHAR(10),
        EMAIL NOT NULL VARCHAR(45),
        CONSTRAINT buyer_no_unique UNIQUE (BUYER_NO)
        )
    """,
    "CUSTOMER_GLOBAL": """
    CREATE TABLE CUSTOMER_GLOBAL(
        CUSTOMER_NO INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME NOT NULL VARCHAR(45),
        ADDRESS NOT NULL VARCHAR(45),
        PHONE NOT NULL CHAR(10),
        EMAIL NOT NULL VARCHAR(45),
        CONSTRAINT buyer_no_unique UNIQUE (BUYER_NO)
        )
    """,
    "AVAILABLE_AUTO": """
    CREATE TABLE AVAILABLE_AUTO(
        SERIAL_NO INTEGER PRIMARY KEY,
        MODEL NOT NULL VARCHAR(45),
        COLOR NOT NULL VARCHAR(45),
        DEALER NOT NULL VARCHAR(45),
        FOREIGN KEY (MODEL) REFERENCES MODEL(MODEL),
        CONSTRAINT serial_no_unique UNIQUE (SERIAL_NO)
        )
    """,
    "SALES": """
    CREATE TABLE SALES(
        TRANSACTION_NO INTEGER PRIMARY KEY AUTOINCREMENT,
        REP_NO NOT NULL INTEGER,
        CUSTOMER_NO NOT NULL INTEGER,
        VEH_NO NOT NULL INTEGER,
        TRANS_DATE NOT NULL DATE,
        FOREIGN KEY (REP_NO) REFERENCES SALESPERSON(REP_NO),
        FOREIGN KEY (CUSTOMER_NO) REFERENCES CUSTOMER_GLOBAL(CUSTOMER_NO),
        FOREIGN KEY (VEH_NO) REFERENCES AVAILABLE_AUTO(SERIAL_NO),
        CONSTRAINT transaction_no_unique UNIQUE (TRANSACTION_NO)
        )
    """,
    "REBATE_GLOBAL": """
    CREATE TABLE REBATE_GLOBAL(
        MODEL VARCHAR(45) PRIMARY KEY,
        AMOUNT NOT NULL DECIMAL(20, 2) DEFAULT 0,
        DEALER NOT NULL VARCHAR(45),
        START_DATE NOT NULL DATE,
        END_DATE NULL DATE,
        FOREIGN KEY (MODEL) REFERENCES MODEL(MODEL)
        )
    """
}

"""
INSERT Fake Data
"""
global_insert_data = {
    "insert_global_model": [
        """
        INSERT INTO MODEL VALUES(
            "Tacoma",
            22000,
            "Truck",
            20,
            7,
            4.0
            )
        """,
        """
        INSERT INTO MODEL VALUES(
            "Tundra",
            20000,
            "Truck",
            22,
            7,
            4.0
            )
        """
    ],
    "insert_global_users": [
        'INSERT INTO users VALUES("admin", "admin")'
    ]
}
