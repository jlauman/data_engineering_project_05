class SqlCreates:
    aaa_drop = ("""
        DROP TABLE IF EXISTS public.staging_events;
        DROP TABLE IF EXISTS public.staging_songs;
        DROP TABLE IF EXISTS public.songplays;
        DROP TABLE IF EXISTS public.artists;
        DROP TABLE IF EXISTS public.songs;
        DROP TABLE IF EXISTS public.times;
        DROP TABLE IF EXISTS public.users;
    """)

    staging_events = ("""
        CREATE TABLE IF NOT EXISTS public.staging_events (
            artist varchar(256),
            auth varchar(256),
            firstname varchar(256),
            gender varchar(256),
            iteminsession int4,
            lastname varchar(256),
            length numeric(18,0),
            "level" varchar(256),
            location varchar(256),
            "method" varchar(256),
            page varchar(256),
            registration numeric(18,0),
            sessionid int4,
            song varchar(256),
            status int4,
            ts int8,
            useragent varchar(256),
            userid int4
        );
    """)

    staging_songs = ("""
        CREATE TABLE IF NOT EXISTS public.staging_songs (
            num_songs int4,
            artist_id varchar(256),
            artist_name varchar(256),
            artist_latitude numeric(18,0),
            artist_longitude numeric(18,0),
            artist_location varchar(256),
            song_id varchar(256),
            title varchar(256),
            duration numeric(18,0),
            "year" int4
        );
    """)

    artists = ("""
        CREATE TABLE IF NOT EXISTS public.artists (
            artistid varchar(256) NOT NULL,
            name varchar(256),
            location varchar(256),
            lattitude numeric(18,0),
            longitude numeric(18,0)
        );
    """)

    songplays = ("""
        CREATE TABLE IF NOT EXISTS public.songplays (
            playid varchar(32) NOT NULL,
            start_time timestamp NOT NULL,
            userid int4 NOT NULL,
            "level" varchar(256),
            songid varchar(256),
            artistid varchar(256),
            sessionid int4,
            location varchar(256),
            user_agent varchar(256),
            CONSTRAINT songplays_pkey PRIMARY KEY (playid)
        );
    """)

    songs = ("""
        CREATE TABLE IF NOT EXISTS public.songs (
            songid varchar(256) NOT NULL,
            title varchar(256),
            artistid varchar(256),
            "year" int4,
            duration numeric(18,0),
            CONSTRAINT songs_pkey PRIMARY KEY (songid)
        );
    """)

    times = ("""
        CREATE TABLE IF NOT EXISTS public.times (
            start_time timestamp NOT NULL,
            hour int4,
            day int4,
            week int4,
            month int4,
            year int4,
            dayofweek int4,
            CONSTRAINT start_time_pkey PRIMARY KEY (start_time)
        );
    """)

    users = ("""
        CREATE TABLE IF NOT EXISTS public.users (
            userid int4 NOT NULL,
            first_name varchar(256),
            last_name varchar(256),
            gender varchar(256),
            "level" varchar(256),
            CONSTRAINT users_pkey PRIMARY KEY (userid)
        );
    """)

    zzz_truncate = ("""
        TRUNCATE TABLE public.staging_events;
        TRUNCATE TABLE public.staging_songs;
        TRUNCATE TABLE public.songplays;
        TRUNCATE TABLE public.artists;
        TRUNCATE TABLE public.songs;
        TRUNCATE TABLE public.times;
        TRUNCATE TABLE public.users;
    """)
