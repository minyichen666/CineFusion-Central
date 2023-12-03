DROP DATABASE movie_db;

CREATE DATABASE movie_db;

USE movie_db;

CREATE TABLE NetflixTitles (
    show_id INT NOT NULL,
    type VARCHAR(255),
    title VARCHAR(255),
    country VARCHAR(255),
    date_added DATE,
    release_year INT,
    duration INT,
    cast VARCHAR(255),
    listed_in VARCHAR(255)
);

LOAD DATA INFILE '/var/lib/mysql-files/new_netflix_titles.csv' INTO TABLE NetflixTitles FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

CREATE TABLE TvShows (
    title VARCHAR(255) PRIMARY KEY NOT NULL,
    Year INT NOT NULL,
    Age INT,
    IMDb INT,
    `Rotten Tomatoes` INT NOT NULL
);

LOAD DATA INFILE '/var/lib/mysql-files/new_tv_shows.csv' INTO TABLE TvShows FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES;

DELETE FROM
    TvShows
WHERE
    title NOT IN (
        SELECT
            DISTINCT title
        FROM
            NetflixTitles
    );

DELETE FROM
    NetflixTitles
WHERE
    title NOT IN (
        SELECT
            DISTINCT title
        FROM
            TvShows
    );

CREATE TABLE Movie (
    movie_id INT PRIMARY KEY NOT NULL,
    type VARCHAR(255),
    title VARCHAR(255),
    country VARCHAR(255),
    date_added DATE,
    release_year INT,
    duration INT,
    CHECK (
        duration > 0
        AND duration <= 600
    )
);

INSERT INTO
    Movie (
        movie_id,
        type,
        title,
        country,
        date_added,
        release_year,
        duration
    )
SELECT
    DISTINCT show_id,
    type,
    title,
    country,
    date_added,
    release_year,
    duration
FROM
    NetflixTitles;

CREATE INDEX idx_movie_title ON Movie(title);

CREATE TABLE Actor (
    actor_name VARCHAR(255) PRIMARY KEY NOT NULL
);

INSERT INTO Actor (actor_name)
SELECT DISTINCT cast
FROM (
    SELECT cast
    FROM NetflixTitles
) AS ActorData;

CREATE TABLE RatingPlatform (
    platform_name VARCHAR(255) PRIMARY KEY NOT NULL
);

INSERT INTO
    RatingPlatform (platform_name)
VALUES
    ('IMDb');

INSERT INTO
    RatingPlatform (platform_name)
VALUES
    ('Rotten Tomatoes');

CREATE TABLE User (
    Username VARCHAR(255) PRIMARY KEY NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_description VARCHAR(255),
    user_attributes VARCHAR(255),
    num_of_followers INT
);

INSERT INTO
    User (
        Username,
        password,
        user_description,
        user_attributes,
        num_of_followers
    )
VALUES
    ('Zishun', 'Zishun', 'none', 'none', 0),
    ('Bowen', 'Bowen', 'none', 'none', 0),
    ('Minyi', 'Minyi', 'none', 'none', 0),
    ('Sarah', 'Sarah', 'none', 'none', 0),
    ('Michael', 'Michael', 'none', 'none', 0),
    ('Emily', 'Emily', 'none', 'none', 0),
    ('David', 'David', 'none', 'none', 0),
    ('Jessica', 'Jessica', 'none', 'none', 0),
    ('Christopher', 'Christopher', 'none', 'none', 0),
    ('Olivia', 'Olivia', 'none', 'none', 0);

CREATE TABLE Watchlist (
    Username VARCHAR(255),
    title VARCHAR(255),
    movie_id INT,
    FOREIGN KEY (Username) REFERENCES User(Username),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
);

INSERT INTO Watchlist (Username,title, movie_id) 
SELECT
    u.Username,
    m.title,
    m.movie_id
FROM
    User u
    CROSS JOIN Movie m
WHERE
    RAND() <= 0.5  
LIMIT 20;  


CREATE TABLE ActsIn (
    movie_id INT,
    actor_name VARCHAR(255),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (actor_name) REFERENCES Actor(actor_name)
);

INSERT
    IGNORE INTO ActsIn (movie_id, actor_name)
SELECT
    show_id,
    CAST(cast AS CHAR)
FROM
    NetflixTitles;

CREATE TABLE Genre (genre VARCHAR(255) PRIMARY KEY NOT NULL);

INSERT INTO
    Genre (genre)
SELECT
    DISTINCT LOWER(listed_in) AS genre
FROM
    NetflixTitles;

CREATE TABLE GenreIn (
    movie_id INT,
    genre VARCHAR(255),
    PRIMARY KEY (movie_id, genre), 
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (genre) REFERENCES Genre(genre)
);

INSERT
    IGNORE INTO GenreIn (movie_id, genre)
SELECT
    show_id,
    LOWER(listed_in) AS genre
FROM
    NetflixTitles;

CREATE TABLE PlatformRating (
    title VARCHAR(255),
    platform_name VARCHAR(255),
    rating FLOAT,
    CHECK (
        rating >= 0
        AND rating <= 100
    ),
    PRIMARY KEY (title, platform_name),
    FOREIGN KEY (platform_name) REFERENCES RatingPlatform(platform_name),
    FOREIGN KEY (title) REFERENCES Movie(title)
);

INSERT INTO
    PlatformRating (title, platform_name, rating)
SELECT
    title,
    'IMDb',
    IMDb
FROM
    TvShows;

INSERT INTO
    PlatformRating (title, platform_name, rating)
SELECT
    title,
    'Rotten Tomatoes',
    'Rotten Tomatoes'
FROM
    TvShows;

CREATE TABLE Friend (
    username1 VARCHAR(255),
    username2 VARCHAR(255),
    FOREIGN KEY (username1) REFERENCES User(Username),
    FOREIGN KEY (username2) REFERENCES User(Username)
);