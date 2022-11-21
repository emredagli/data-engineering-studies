import configparser
import psycopg2
from sql_queries import unload_queries


def unload_tables(cur, conn):
    """
    It unloads "staging_songs" table content to another S3 bucket.
    Please check the query function to get more detail.
    @param cur: Connected Database cursor instance.
    @param conn: Connected Database connection instance.
    @return: void
    """
    for query in unload_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main unload Redshift staging songs table function.
    Before executing this function you need to fill the staging tables and define "SONG_DATA_UNLOAD" path on "./dwh.cfg"
    - It connects to the Redshift database by using the configs defined on "dwh.cfg" config file.
    - Then it executes unload tables
    @return: void
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    unload_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
