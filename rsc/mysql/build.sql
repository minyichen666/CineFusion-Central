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
    cast VARCHAR(1000),
    listed_in VARCHAR(255)
);

LOAD DATA INFILE '/var/lib/mysql-files/new_netflix_titles.csv'
INTO TABLE NetflixTitles
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE Movie (
    movie_id INT PRIMARY KEY NOT NULL,
    type VARCHAR(255),
    title VARCHAR(255),
    country VARCHAR(255),
    date_added DATE,
    release_year INT,
    duration INT,
    CHECK (YEAR(date_added) >= release_year),
    CHECK (duration > 0 AND duration <= 600)
);

INSERT INTO Movie (movie_id, type, title, country, date_added, release_year, duration)
SELECT show_id, type, title, country, date_added, release_year, duration
FROM NetflixTitles;

CREATE TABLE Actor (
    actor_id INT PRIMARY KEY NOT NULL,
    actor_name VARCHAR(255) NOT NULL
);

INSERT INTO Actor (actor_id, actor_name)
SELECT DISTINCT actor_id, actor_name
FROM (
    SELECT show_id, actor_id, actor_name
    FROM NetflixTitles
) AS ActorData;

CREATE TABLE Director (
    director_id INT PRIMARY KEY NOT NULL,
    director_name VARCHAR(255) NOT NULL
);

INSERT INTO Director (director_id, director_name)
SELECT DISTINCT director_id, director_name
FROM (
    SELECT show_id, director_id, director_name
    FROM NetflixTitles
) AS DirectorData;

CREATE TABLE RatingPlatform (
    platform_id INT PRIMARY KEY NOT NULL,
    platform_name VARCHAR(255) NOT NULL
);

INSERT INTO RatingPlatform (platform_id, platform_name)
VALUES (1, 'Netflix');

CREATE TABLE User (
    Username VARCHAR(255) PRIMARY KEY NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_description VARCHAR(255),
    user_attributes VARCHAR(255),
    num_of_followers INT
);

CREATE TABLE Watchlist (
    Username VARCHAR(255),
    ID INT,
    PRIMARY KEY (Username, ID),
    FOREIGN KEY (Username) REFERENCES User(Username),
    UNIQUE (ID)
);

CREATE TABLE ActsIn (
    movie_id INT,
    actor_id INT,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (actor_id) REFERENCES Actor(actor_id)
);

INSERT INTO ActsIn (movie_id, actor_id)
SELECT show_id, actor_id
FROM NetflixTitles;

CREATE TABLE Directs (
    movie_id INT,
    director_id INT,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (director_id) REFERENCES Director(director_id)
);

INSERT INTO Directs (movie_id, director_id)
SELECT show_id, director_id
FROM NetflixTitles;

CREATE TABLE PlatformRating (
    movie_id INT,
    platform_id INT,
    rating FLOAT,
    CHECK (rating >= 0 AND rating <= 10),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (platform_id) REFERENCES RatingPlatform(platform_id)
);

INSERT INTO PlatformRating (movie_id, platform_id, rating)
SELECT show_id, 1, CAST(rating AS DECIMAL(4, 2))
FROM NetflixTitles;

CREATE TABLE Watch (
    Username VARCHAR(255),
    ID INT,
    movie_ID INT,
    watch_times INT,
    FOREIGN KEY (Username) REFERENCES User(Username),
    FOREIGN KEY (ID) REFERENCES Watchlist(ID),
    FOREIGN KEY (movie_ID) REFERENCES Movie(movie_id)
);

CREATE TABLE Friend (
    username1 VARCHAR(255),
    username2 VARCHAR(255),
    FOREIGN KEY (username1) REFERENCES User(Username),
    FOREIGN KEY (username2) REFERENCES User(Username)
);