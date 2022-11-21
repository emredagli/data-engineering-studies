import psycopg2
from sql_queries import create_table_queries, drop_table_queries

DEFAULT_DB_NAME = "studentdb"
DEFAULT_DB_USER = "emrelocal"
DEFAULT_DB_PASSWORD = ""

SPARKIFY_DB_NAME = "sparkifydb"
SPARKIFY_DB_USER = DEFAULT_DB_USER
SPARKIFY_DB_PASSWORD = DEFAULT_DB_PASSWORD

DEFAULT_DB_CONNECTION_STRING = f"host=127.0.0.1 dbname={DEFAULT_DB_NAME} user={DEFAULT_DB_USER} password={DEFAULT_DB_PASSWORD}"
SPARKIFY_DB_CONNECTION_STRING = f"host=127.0.0.1 dbname={SPARKIFY_DB_NAME} user={SPARKIFY_DB_USER} password={SPARKIFY_DB_PASSWORD}"

def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    # connect to default database
    conn = psycopg2.connect(DEFAULT_DB_CONNECTION_STRING)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute(f"DROP DATABASE IF EXISTS {SPARKIFY_DB_NAME}")
    cur.execute(f"CREATE DATABASE {SPARKIFY_DB_NAME} WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(SPARKIFY_DB_CONNECTION_STRING)
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
