import sqlite3
from sqlite3 import Error
import os

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def initialize_database(db_file):
    sql_create_root_users_table = """
    CREATE TABLE IF NOT EXISTS root_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        alias TEXT
    );
    """

    conn = create_connection(db_file)

    if conn is not None:
        create_table(conn, sql_create_root_users_table)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

def create_customer_table(conn, customer_name):
    sql_create_customer_table = f"""
    CREATE TABLE IF NOT EXISTS '{customer_name}' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        items TEXT,
        amount REAL NOT NULL,
        phrase TEXT,
        total REAL NOT NULL
    );
    """
    create_table(conn, sql_create_customer_table)

def add_root_user(conn, customer_name, alias=None):
    # Check if the user already exists
    check_sql = "SELECT * FROM root_users WHERE customer_name = ?"
    cur = conn.cursor()
    cur.execute(check_sql, (customer_name,))
    if cur.fetchone():
        print(f"User {customer_name} already exists.")
        return None  # or return an appropriate value/message indicating duplication

    # If user does not exist, insert new user
    insert_sql = ''' INSERT INTO root_users(customer_name,alias)
                     VALUES(?,?) '''
    cur.execute(insert_sql, (customer_name, alias))
    conn.commit()
    return cur.lastrowid

def add_customer_entry(conn, customer_name, date, items, amount, phrase, total):
    sql = f''' INSERT INTO '{customer_name}'(date,items,amount,phrase,total)
               VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (date, items, amount, phrase, total))
    conn.commit()
    return cur.lastrowid

# Usage example:
if __name__ == '__main__':

    current_dir= os.getcwd()
    db_file = os.path.join(current_dir,r"src\borrowing_ledger\database","borrowing_ledger.db")
    print(db_file)
    initialize_database(db_file)
    
    conn = create_connection(db_file)
    if conn is not None:
        add_root_user(conn, "John Doe", "Johnny")
        create_customer_table(conn, "John Doe")
        add_customer_entry(conn, "John Doe", "2023-07-17", "Book", 20.5, "Borrowed for study", 20.5)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")