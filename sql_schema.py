"""
CREATE Global Tables
"""
global_tables = {
    "MODEL": """
    CREATE TABLE MODEL(
        MODEL VARCHAR(20),
        PRICE DECIMAL(20, 2),
        TYPE VARCHAR(12),
        GAS_MILEAGE SMALLINT,
        SEAT SMALLINT,
        ENGINE DECIMAL(2,1)
        )
    """,
    "users": """CREATE TABLE users(username TEXT, password TEXT)""",
    "ADD_ON": """
    CREATE TABLE ADD_ON(
        PACKAGE_NO VARCHAR(4),
        PACKAGE_DESCRIPTION VARCHAR(20),
        PRICE DECIMAL(20, 2),
        MODEL_AVAILABLE VARCHAR(30)
        )
    """,

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
