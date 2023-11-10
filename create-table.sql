DROP DATABASE movie_db;
CREATE DATABASE movie_db;
USE movie_db;
CREATE TABLE Movie (
    movie_id INT PRIMARY KEY NOT NULL,
    type VARCHAR(255),
    title VARCHAR(255),
    country VARCHAR(255),
    date_added DATE,
    releasing_year INT,
    duration INT,
    CHECK (YEAR(date_added) >= releasing_year),
    CHECK (duration > 0 AND duration <= 600)
);

CREATE TABLE Actor (
    actor_id INT PRIMARY KEY NOT NULL,
    actor_name VARCHAR(255) NOT NULL
);

CREATE TABLE Director (
    director_id INT PRIMARY KEY NOT NULL,
    director_name VARCHAR(255) NOT NULL
);

CREATE TABLE RatingPlatform (
    platform_id INT PRIMARY KEY NOT NULL,
    platform_name VARCHAR(255) NOT NULL
);

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

-- Define relation sets
CREATE TABLE ActsIn (
    movie_id INT,
    actor_id INT,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (actor_id) REFERENCES Actor(actor_id)
);

CREATE TABLE Directs (
    movie_id INT,
    director_id INT,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (director_id) REFERENCES Director(director_id)
);

CREATE TABLE PlatformRating (
    movie_id INT,
    platform_id INT,
    rating FLOAT,
    CHECK (rating >= 0 AND rating <= 10),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (platform_id) REFERENCES RatingPlatform(platform_id)
);

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
