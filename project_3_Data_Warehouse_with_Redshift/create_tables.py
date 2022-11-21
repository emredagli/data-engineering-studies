import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop Tables Function.
    - It drops all staging and DWH analytical tables.
    @param cur: Connected Database cursor instance.
    @param conn: Connected Database connection instance.
    @return: void
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create Tables Function.
    - It creates all staging and DWH analytical tables.
    @param cur: Connected Database cursor instance.
    @param conn: Connected Database connection instance.
    @return: void
    """
    for query in create_table_queries:
        if query.strip() == "":
            continue
        cur.execute(query)
        conn.commit()


def main():
    """
    Main Create Tables Functions
    - It connects to the Redshift database by using the configs defined on "dwh.cfg" config file.
    - It drops and then creates all staging and DWH analytical tables.
    @return: void
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
