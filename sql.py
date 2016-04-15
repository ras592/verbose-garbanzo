import sqlite3

def run_sql():
    with sqlite3.connect("sample.db") as connection:
        c = connection.cursor()
        create_test_table(c)
        create_basic_user_accts(c)

def create_test_table(c):
    c.execute("""CREATE TABLE tests(title TEXT, description TEXT)""")
    c.execute('INSERT INTO tests VALUES("Test 1", "Hello, World!")')
    c.execute('INSERT INTO tests VALUES("Test 2", "Well, hi.")')

def create_basic_user_accts(c):
    c.execute("""CREATE TABLE users(username TEXT, password TEXT)""")
    c.execute('INSERT INTO users VALUES("admin", "admin")')

run_sql()
