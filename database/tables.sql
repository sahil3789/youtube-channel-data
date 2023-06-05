CREATE TABLE IF NOT EXISTS channel_data(
        dtype VARCHAR(255),
        channel_id VARCHAR(255),
        channel_title VARCHAR(255),
        channel_description VARCHAR(10000),
        view_count BIGINT,
        video_count BIGINT,
        status VARCHAR(255));

CREATE TABLE IF NOT EXISTS video_data(
        dtype VARCHAR(255),
        video_id VARCHAR(255),
        channel_id VARCHAR(255),
        video_title VARCHAR(255),
        video_description VARCHAR(10000),
        published_date VARCHAR(255),
        thumbnail VARCHAR(255),
        duration_min FLOAT,
        view_count BIGINT,
        like_count BIGINT,
        favourite_count BIGINT,
        comment_count BIGINT);

CREATE TABLE IF NOT EXISTS playlist_data(
       dtype VARCHAR(255),
       channel_id VARCHAR(255),
       playlist_id VARCHAR(255),
       playlist_title VARCHAR(255));

CREATE TABLE IF NOT EXISTS comment_data(
        dtype VARCHAR(255),
        comment_id VARCHAR(255),
        video_id VARCHAR(255),
        comment_text VARCHAR(255),
        comment_author VARCHAR(255),
        publisehd_date VARCHAR(255));
