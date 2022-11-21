import configparser
import psycopg2
import time
from sql_queries import copy_table_queries, insert_table_queries


# ETL JOB Stats:

# 8 multi nodes cluster:
# staging_songs     2347.4207260608673 seconds
# staging_events    2.696377992630005 seconds
# songplays         1.1326091289520264 seconds
# users             0.8813810348510742 seconds
# songs             1.0608139038085938 seconds
# artists           1.1687641143798828 seconds
# time              0.9314279556274414 seconds

# 1 single-node cluster (using unloaded song data: staging_songs_copy_bulk):
# staging_songs     6.8602070808410645 seconds
# staging_events    4.963327884674072 seconds
# songplays         0.9634740352630615 seconds
# users             0.8754050731658936 seconds
# songs             0.9712491035461426 seconds
# artists           0.9386749267578125 seconds
# time              0.8383951187133789 seconds


def load_staging_tables(cur, conn):
    """
    Load Staging Tables Function.
    - It loads 2 staging tables: staging_songs, staging_events from s3 URIs
    @param cur: Connected Database cursor instance.
    @param conn: Connected Database connection instance.
    @return: void
    """
    for query in copy_table_queries:
        # start_time = time.time()
        cur.execute(query)
        conn.commit()
        # print(query)
        # print("%s seconds\n ------------" % (time.time() - start_time))


def insert_tables(cur, conn):
    """
    Insert Tables Function.
    - It loads DWH Analytical Tables: songplays, users, songs, artists, time from staging tables
    @param cur: Connected Database cursor instance.
    @param conn: Connected Database connection instance.
    @return: void
    """
    for query in insert_table_queries:
        # start_time = time.time()
        cur.execute(query)
        conn.commit()
        # print(query)
        # print("%s seconds\n ------------" % (time.time() - start_time))


def main():
    """
    It is our main ETL pipeline.
    - It connects to the Redshift database by using the configs defined on "dwh.cfg" config file.
    - It (E)xtracts data from S3 buckets to staging tables (load_staging_tables function)
    - It (T)ransfers and (L)oads data from staging tables to DWH Analytical Tables (insert_tables)
    @return: void
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
