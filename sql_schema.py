"""
sql_schema
File stores all of the SQL models
replace _ with space and captialize the first letter
"""

"""
CREATE Global Tables
"""
# because order matters enter in the tables into the order of the tuple
global_tables_tuple = ("users", "model", "add_on", "employee",
                        "salesperson", "potential_buyer", "customer_global",
                        "available_auto", "sales", "rebate_global")
global_tables = {
    "model": """
    CREATE TABLE global.model(
        model VARCHAR(45) PRIMARY KEY,
        price DECIMAL(20, 2) NOT NULL,
        type VARCHAR(45) NOT NULL,
        gas_mileage SMALLINT NOT NULL,
        seat SMALLINT NOT NULL,
        engine DECIMAL(2,1) NOT NULL,
        UNIQUE INDEX model_unique (model)
        )
    """,
    "users": """
    CREATE TABLE global.users(
        username VARCHAR(45) PRIMARY KEY,
        password CHAR(40) NOT NULL,
        UNIQUE INDEX username_unique (username)
        )
    """,
    "add_on": """
    CREATE TABLE global.add_on(
        package_no VARCHAR(4) PRIMARY KEY,
        package_description VARCHAR(45) NOT NULL,
        price DECIMAL(20, 2) NOT NULL,
        model_available VARCHAR(45) NOT NULL,
        model VARCHAR(45) NOT NULL,
        FOREIGN KEY (model) REFERENCES global.model(model),
        UNIQUE INDEX package_no_unique (package_no)
        )
    """,
    "employee": """
    CREATE TABLE global.employee(
        emp_no INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(45) NOT NULL,
        address VARCHAR(45) NOT NULL,
        phone CHAR(10) NOT NULL,
        position VARCHAR(45) NOT NULL,
        UNIQUE INDEX emp_no_unique (emp_no ASC)
        )
    """,
    "salesperson": """
    CREATE TABLE global.salesperson(
        rep_no INT PRIMARY KEY,
        base_salary DECIMAL(20, 2) DEFAULT 0  NOT NULL,
        ytd_sales DECIMAL(20, 2) DEFAULT 0  NOT NULL,
        comm DECIMAL(20, 2) DEFAULT 0  NOT NULL,
        FOREIGN KEY (rep_no) REFERENCES global.employee(emp_no),
        UNIQUE INDEX rep_no_unique (rep_no)
    )
    """,
    "potential_buyer": """
    CREATE TABLE global.potential_buyer(
        buyer_no INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(45) NOT NULL,
        address VARCHAR(45) NOT NULL,
        phone CHAR(10) NOT NULL,
        email VARCHAR(45) NOT NULL,
        UNIQUE INDEX buyer_no_unique (buyer_no)
        )
    """,
    "customer_global": """
    CREATE TABLE global.customer_global(
        customer_no INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(45) NOT NULL,
        address VARCHAR(45) NOT NULL,
        phone CHAR(10) NOT NULL,
        email VARCHAR(45) NOT NULL,
        UNIQUE INDEX customer_no_unique (customer_no)
        )
    """,
    "available_auto": """
    CREATE TABLE global.available_auto(
        serial_no INT PRIMARY KEY,
        model VARCHAR(45) NOT NULL,
        color VARCHAR(45) NOT NULL,
        dealer VARCHAR(45) NOT NULL,
        FOREIGN KEY (model) REFERENCES global.model(model),
        UNIQUE INDEX serial_no_unique (serial_no)
        )
    """,
    "sales": """
    CREATE TABLE global.sales(
        transaction_no INT PRIMARY KEY AUTO_INCREMENT,
        rep_no INT NOT NULL,
        customer_no INT NOT NULL,
        veh_no INT NOT NULL,
        trans_date DATETIME NOT NULL,
        FOREIGN KEY (rep_no) REFERENCES global.salesperson(rep_no),
        FOREIGN KEY (customer_no) REFERENCES global.customer_global(customer_no),
        FOREIGN KEY (veh_no) REFERENCES global.available_auto(serial_no),
        UNIQUE INDEX transaction_no_unique (transaction_no)
        )
    """,
    "rebate_global": """
    CREATE TABLE global.rebate_global(
        model VARCHAR(45) PRIMARY KEY,
        amount DECIMAL(20, 2) DEFAULT 0 NOT NULL,
        dealer VARCHAR(45) NOT NULL,
        start_date DATETIME NOT NULL,
        end_date DATETIME NULL,
        FOREIGN KEY (model) REFERENCES global.model(model)
        )
    """
}

"""
CREATE Local 1 Tables
"""
stlouis_tables_tuple = ("cars", "representative", "customer_d1", "transaction",
                        "rebate1", "loan")
stlouis_tables = {
    "cars": """
    CREATE TABLE local_sl.cars(
        serialno INT PRIMARY KEY,
        model VARCHAR(45) NOT NULL,
        color VARCHAR(45) NOT NULL,
        autotrans VARCHAR(3) NOT NULL,
        warehouse VARCHAR(45) NOT NULL,
        FOREIGN KEY (model) REFERENCES global.model(model),
        UNIQUE INDEX serialno_unique (serialno)
        )
    """,
    "representative": """
        CREATE TABLE local_sl.representative(
            rep_no INT PRIMARY KEY,
            name VARCHAR(45) NOT NULL,
            address VARCHAR(45) NOT NULL,
            phone CHAR(10) NOT NULL,
            base_salary DECIMAL(20, 2) DEFAULT 0  NOT NULL,
            ytd_sales DECIMAL(20, 2) DEFAULT 0  NOT NULL,
            comm DECIMAL(20, 2) DEFAULT 0  NOT NULL,
            FOREIGN KEY (rep_no) REFERENCES global.salesperson(rep_no),
            UNIQUE INDEX rep_no_unique (rep_no)
        )
    """,
    "customer_d1": """
    CREATE TABLE local_sl.`customer_d1`(
        customer_no INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(45) NOT NULL,
        address VARCHAR(45) NOT NULL,
        phone CHAR(10) NOT NULL,
        email VARCHAR(45) NOT NULL,
        UNIQUE INDEX customer_no_unique (customer_no)
        )
    """,
    "rebate1": """
    CREATE TABLE local_sl.`rebate1`(
        model VARCHAR(45) PRIMARY KEY,
        amount DECIMAL(20, 2) NOT NULL,
        start_date DATETIME NOT NULL,
        end_date DATETIME NULL,
        FOREIGN KEY (model) REFERENCES global.model(model)
        )
    """,
    "loan": """
    CREATE TABLE local_sl.loan(
        serialno INT PRIMARY KEY,
        amount DECIMAL(20, 2) NOT NULL,
        start_date DATETIME NOT NULL,
        end_date DATETIME NULL,
        FOREIGN KEY (serialno) REFERENCES local_sl.cars(serialno),
        UNIQUE INDEX serialno_unique (serialno)
        )
    """,
    "transaction": """
    CREATE TABLE local_sl.transaction(
        deal_no INT PRIMARY KEY AUTO_INCREMENT,
        rep_no INT NOT NULL,
        customer_no INT NOT NULL,
        serialno INT NOT NULL,
        amount DECIMAL(20, 2) DEFAULT 0 NOT NULL,
        fin_amt DECIMAL(20, 2) DEFAULT 0 NOT NULL,
        `date` DATETIME NOT NULL,
        rebate_amt DECIMAL(20, 2) DEFAULT 0 NOT NULL,
        FOREIGN KEY (rep_no) REFERENCES local_sl.representative(rep_no),
        FOREIGN KEY (customer_no) REFERENCES local_sl.customer_d1(customer_no),
        FOREIGN KEY (serialno) REFERENCES local_sl.cars(serialno),
        UNIQUE INDEX deal_no_unique (deal_no)
        )
    """
}

"""
CREATE Local 2 Tables
"""
kansascity_tables_tuple = ("autos", "sales_person", "customer_d2", "deal",
                        "rebate2", "finance")
kansascity_tables = {
    "autos": """
    CREATE TABLE local_kc.autos(
        vehicle_no INT PRIMARY KEY,
        model VARCHAR(45) NOT NULL,
        color VARCHAR(45) NOT NULL,
        autotrans VARCHAR(3) NOT NULL,
        warehouse VARCHAR(45) NOT NULL,
        financed VARCHAR(3) NOT NULL,
        FOREIGN KEY (model) REFERENCES global.model(model),
        UNIQUE INDEX vehicle_no_unique (vehicle_no)
        )
    """,
    "sales_person": """
    CREATE TABLE local_kc.sales_person(
        sale_no INT PRIMARY KEY,
        name VARCHAR(45) NOT NULL,
        address VARCHAR(45) NOT NULL,
        phone CHAR(10) NOT NULL,
        base_salary DECIMAL(20, 2) DEFAULT 0  NOT NULL,
        ytdsales DECIMAL(20, 2) DEFAULT 0  NOT NULL,
        comm DECIMAL(20, 2) DEFAULT 0  NOT NULL,
        FOREIGN KEY (sale_no) REFERENCES global.salesperson(rep_no),
        UNIQUE INDEX sale_no_unique (sale_no)
        )
    """,
    "customer_d2": """
    CREATE TABLE local_kc.`customer_d2`(
        buyer_no INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(45) NOT NULL,
        address VARCHAR(45) NOT NULL,
        phone CHAR(10) NOT NULL,
        email VARCHAR(45) NOT NULL,
        UNIQUE INDEX buyer_no_unique (buyer_no)
        )
    """,
    "rebate2": """
    CREATE TABLE local_kc.`rebate2`(
        model VARCHAR(45) PRIMARY KEY,
        amount DECIMAL(20, 2) NOT NULL,
        start_date DATETIME NOT NULL,
        end_date DATETIME NULL,
        FOREIGN KEY (model) REFERENCES global.model(model)
        )
    """,
    "finance": """
    CREATE TABLE local_kc.finance(
        vehicle_no INT PRIMARY KEY,
        buyer_no INT NOT NULL,
        amount DECIMAL(20, 2) NOT NULL,
        months SMALLINT NOT NULL,
        balance DECIMAL(20, 2) NOT NULL,
        FOREIGN KEY (vehicle_no) REFERENCES local_kc.autos(vehicle_no),
        FOREIGN KEY (buyer_no) REFERENCES local_kc.customer_d2(buyer_no),
        UNIQUE INDEX vehicle_no_unique (vehicle_no)
        )
    """,
    "deal": """
    CREATE TABLE local_kc.deal(
        deal_no INT PRIMARY KEY AUTO_INCREMENT,
        rep_no INT NOT NULL,
        customer_no INT NOT NULL,
        serial_no INT NOT NULL,
        amount DECIMAL(20, 2) DEFAULT 0 NOT NULL,
        fin_amt DECIMAL(20, 2) DEFAULT 0 NOT NULL,
        `date` DATETIME NOT NULL,
        rebate_amt DECIMAL(20, 2) DEFAULT 0 NOT NULL,
        FOREIGN KEY (rep_no) REFERENCES local_kc.sales_person(sale_no),
        FOREIGN KEY (customer_no) REFERENCES local_kc.customer_d2(buyer_no),
        FOREIGN KEY (serial_no) REFERENCES local_kc.autos(vehicle_no),
        UNIQUE INDEX deal_no_unique (deal_no)
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
        'INSERT INTO global.users VALUES("admin", SHA("admin"))',
        'INSERT INTO global.users VALUES("user1", SHA("pass123"))'
    ]
}
