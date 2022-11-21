import configparser
import psycopg2
from sql_queries import clear_table_queries


def clear_tables(cur, conn):
    """
    Clear Tables Function.
    - It removes all data from DWH Analytical tables
    @param cur: Connected Database cursor instance.
    @param conn: Connected Database connection instance.
    @return: void
    """
    for query in clear_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - It connects to the Redshift database by using the configs defined on "dwh.cfg" config file.
    - It clears the DWH tables content.
    @return: void
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    clear_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
