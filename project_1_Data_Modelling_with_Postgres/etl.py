import os
import glob
import psycopg2
import pandas as pd

from create_tables import drop_tables, create_tables, SPARKIFY_DB_CONNECTION_STRING
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Song file processor function. It fills 'songs' and 'artists' dimension tables by using given single songs JSON file.
    @param cur: Connected Database cursor instance.
    @param filepath: Single song file path
    @return: void
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    for index, row in df.iterrows():
        # insert song record
        song_data = row[["song_id", "title", "artist_id", "year", "duration"]].values.tolist()
        cur.execute(song_table_insert, song_data)
    
        # insert artist record
        artist_data = row[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values.tolist()
        cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Log file processor function.
    - It fills 'time' and 'users' dimension tables first by using given single log JSON file.
    - And then it fills the fact 'songplays' table by using their foreign keys
    @param cur: Connected Database cursor instance.
    @param filepath: Single log file path
    @return: void
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = (df['ts'], t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.dayofweek)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(time_data, column_labels).T

    for i, row in time_df.iterrows():
        # upsert time records
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # upsert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function takes path of the dataset files and processor function.
    It traverses all files under filepath and executes processor function for each dataset.

    @param cur: Connected Database cursor instance.
    @param conn: Connected Database connection instance.
    @param filepath: root path of the JSON formatted datasets.
    @param func: Processor function be executed for each JSON file.
    @return: void
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        print('{}/{} file is started for processing. Filepath: {}'.format(i, num_files, datafile))
        func(cur, datafile)
        conn.commit()


def main(connection_string):
    """
    It is our main pipeline.
    It creates the database and tables.
    And then, it fills the database by using song and log data sets.
    @param connection_string: PostgreSQL Database connection string
    @return: void
    """
    try:
        conn = psycopg2.connect(connection_string)
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database", e)
        return

    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the Database", e)
        return

    conn.set_session(autocommit=True)

    drop_tables(cur, conn)
    create_tables(cur, conn)

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main(SPARKIFY_DB_CONNECTION_STRING)
