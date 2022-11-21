import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# CONFIG VARIABLES
HOST = config.get('CLUSTER', 'HOST')
DB_NAME = config.get('CLUSTER', 'DB_NAME')
DB_USER = config.get('CLUSTER', 'DB_USER')
DB_PASSWORD = config.get('CLUSTER', 'DB_PASSWORD')
DB_PORT = config.get('CLUSTER', 'DB_PORT')

IAM_ROLE_ARN = config.get('IAM_ROLE', 'ARN')

S3_LOG_DATA = config.get('S3', 'LOG_DATA')
S3_LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
S3_SONG_JSONPATH = config.get('S3', 'SONG_JSONPATH')
S3_SONG_DATA = config.get('S3', 'SONG_DATA')
S3_SONG_DATA_UNLOAD = config.get('S3', 'SONG_DATA_UNLOAD')
S3_REGION = config.get('S3', 'REGION')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"

songplay_table_drop = "DROP TABLE IF EXISTS songplays CASCADE;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CLEAR TABLES

songplay_table_clear = "DELETE FROM songplays;"
user_table_clear = "DELETE FROM users;"
song_table_clear = "DELETE FROM songs;"
artist_table_clear = "DELETE FROM artists;"
time_table_clear = "DELETE FROM time;"


# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events
(
    artist          varchar(120), -- <- max len result is 89    
    auth            varchar(16),  -- <- max len result is 10
    first_name      varchar(16),  -- <- max len result is 10
    gender          varchar(1),   -- <- max len result is 1
    item_in_session integer,
    last_name       varchar(16),  -- <- max len result is 9
    length          double precision,
    level           varchar(6),   -- <- max len result is 4
    location        varchar(64),  -- <- max len result is 46
    method          varchar(6),   -- <- max len result is 3 
    page            varchar(24),  -- <- max len result is 16
    registration    BIGINT,
    session_id      integer,
    song            varchar(180), -- <- max len result is 151
    status          integer,
    ts              BIGINT,
    user_agent      varchar(160), -- <- max len result is 139
    user_id         integer
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs
(
    song_id          varchar(18), -- <- max len result is 18
    num_songs        integer,
    title            varchar(300), -- <- max len result is 255
    artist_name      varchar(400), -- <- max len result is 358
    artist_latitude  double precision,
    year             integer,
    duration         double precision,
    artist_id        varchar(18), -- <- max len result is 18
    artist_longitude double precision,
    artist_location  varchar(300) -- <- max len result is 276
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
(
    songplay_id integer IDENTITY NOT NULL PRIMARY KEY,
    start_time  timestamp        NOT NULL SORTKEY, -- <- staging_events.ts
    user_id     integer          NOT NULL,         -- <- staging_events.user_id
    level       varchar(6),                        -- <- staging_events.level
    song_id     varchar(18)      NOT NULL DISTKEY, -- <- staging_songs.song_id
    artist_id   varchar(18)      NOT NULL,         -- <- staging_songs.artist_id
    session_id  integer,                           -- <- staging_events.session_id
    location    varchar(64),                       -- <- staging_events.location
    user_agent  varchar(160),                      -- <- staging_events.user_agent
    FOREIGN KEY (start_time) REFERENCES time (start_time),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (song_id) REFERENCES songs (song_id),
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(
    user_id    integer NOT NULL PRIMARY KEY SORTKEY, -- <- staging_events.user_id
    first_name varchar(16),                          -- <- staging_events.first_name
    last_name  varchar(16),                          -- <- staging_events.last_name
    gender     varchar(1),                           -- <- staging_events.gender
    level      varchar(6)                           -- <- staging_events.level
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs
(
    song_id   varchar(18) NOT NULL PRIMARY KEY SORTKEY DISTKEY, -- <- staging_songs.song_id
    title     varchar(512),                                     -- <- staging_songs.title
    artist_id varchar(18),                                      -- <- staging_songs.artist_id
    year      integer,                                          -- <- staging_songs.year
    duration  double precision                                  -- <- staging_songs.duration
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists
(
    artist_id varchar(18) NOT NULL PRIMARY KEY SORTKEY, -- <- staging_songs.artist_id
    name      varchar(512),                             -- <- staging_songs.artist_name
    location  varchar(512),                             -- <- staging_songs.artist_location
    latitude  double precision,                         -- <- staging_songs.artist_latitude
    longitude double precision                          -- <- staging_songs.artist_longitude
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
(
    start_time timestamp    NOT NULL PRIMARY KEY, -- <- songplays.start_time
    hour       integer   NOT NULL,
    day        integer   NOT NULL,
    week       integer   NOT NULL,
    month      integer   NOT NULL,
    year       integer   NOT NULL,
    weekday    integer   NOT NULL
) SORTKEY(start_time, year, month, day, weekday);
""")

# STAGING TABLES

staging_events_copy = (f"""
COPY staging_events 
    FROM '{S3_LOG_DATA}'
    CREDENTIALS 'aws_iam_role={IAM_ROLE_ARN}'
    JSON '{S3_LOG_JSONPATH}' REGION '{S3_REGION}' COMPUPDATE OFF STATUPDATE OFF;
""")


staging_songs_copy = (f"""
COPY staging_songs
    FROM '{S3_SONG_DATA}'
    CREDENTIALS 'aws_iam_role={IAM_ROLE_ARN}'
    JSON '{S3_SONG_JSONPATH}' REGION '{S3_REGION}' COMPUPDATE OFF STATUPDATE OFF;
""")

staging_songs_copy_bulk = (f"""
COPY staging_songs
    FROM '{S3_SONG_DATA_UNLOAD}'
    CREDENTIALS 'aws_iam_role={IAM_ROLE_ARN}'
    JSON '{S3_SONG_JSONPATH}' REGION '{S3_REGION}' COMPUPDATE OFF STATUPDATE OFF;
""")


# Unload Queries
staging_songs_unload = (f"""
UNLOAD ('SELECT * FROM staging_songs')   
    TO '{S3_SONG_DATA_UNLOAD}' 
    CREDENTIALS 'aws_iam_role={IAM_ROLE_ARN}'
    JSON;
""")

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT timestamp 'epoch' + se.ts / 1000 * interval '1 second' as start_time,
       se.user_id,
       se.level,
       ss.song_id,
       ss.artist_id,       
       se.session_id,
       se.location,
       se.user_agent
FROM staging_events se
INNER JOIN staging_songs ss ON se.song = ss.title AND se.artist = ss.artist_name AND se.length = ss.duration
WHERE se.page = 'NextSong'
  AND se.user_id IS NOT NULL
  AND ss.song_id IS NOT NULL
  AND ss.artist_id IS NOT NULL;
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
SELECT user_id,
       first_name,
       last_name,
       gender,
       level
FROM (SELECT user_id,
             first_name,
             last_name,
             gender,
             level,
             row_number() over (partition by user_id order by ts desc) as rn
      FROM staging_events
      WHERE page = 'NextSong'
        AND user_id IS NOT NULL) se_rn
WHERE rn = 1;
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
SELECT DISTINCT ss.song_id,
                ss.title,
                ss.artist_id,
                ss.year,
                ss.duration
FROM staging_songs ss
INNER JOIN staging_events se ON se.song = ss.title AND se.artist = ss.artist_name AND se.length = ss.duration
WHERE ss.song_id IS NOT NULL AND se.page = 'NextSong';
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
SELECT DISTINCT ss.artist_id,
                ss.artist_name,
                ss.artist_location,
                ss.artist_latitude,
                ss.artist_longitude
FROM staging_songs ss
INNER JOIN staging_events se ON se.song = ss.title AND se.artist = ss.artist_name AND se.length = ss.duration
WHERE ss.artist_id IS NOT NULL AND se.page = 'NextSong';
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT start_time,
                EXTRACT(hour from start_time),
                EXTRACT(day from start_time),
                EXTRACT(week from start_time),
                EXTRACT(month from start_time),
                EXTRACT(year from start_time),
                EXTRACT(dow from start_time)
FROM songplays;
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create,
                        artist_table_create, time_table_create, songplay_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]

# After unloading the staging_songs table, the following line is commented out and the next line is used.
# copy_table_queries = [staging_songs_copy, staging_events_copy]
copy_table_queries = [staging_songs_copy_bulk, staging_events_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

clear_table_queries = [songplay_table_clear, user_table_clear, song_table_clear, artist_table_clear, time_table_clear]

unload_queries = [staging_songs_unload]