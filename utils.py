class Movie:
    def __init__(self, movie_id, type, title, country, date_added, release_year, duration):
        self.movie_id = movie_id
        self.type = type
        self.title = title
        self.country = country
        self.date_added = date_added
        self.release_year = release_year
        self.duration = duration

    def __repr__(self):
        return f"<Movie {self.title}>"

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'type': self.type,
            'title': self.title,
            'country': self.country,
            'date_added': self.date_added,
            'release_year': self.release_year,
            'duration': self.duration
        }
    

class MoviePlatformRating:
    def __init__(self, movie_id, type, title, country, date_added, release_year, duration, platform_name, rating):
        self.movie_id = movie_id
        self.type = type
        self.title = title
        self.country = country
        self.date_added = date_added
        self.release_year = release_year
        self.duration = duration
        self.platform_name = platform_name
        self.rating = rating

    def __repr__(self):
        return f"<Movie {self.title}>"

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'type': self.type,
            'title': self.title,
            'country': self.country,
            'date_added': self.date_added,
            'release_year': self.release_year,
            'duration': self.duration,
            'platform_name': self.platform_name,
            'rating': self.rating
        }
    

class MovieTVShows:
    def __init__(self, movie_id, type, title, country, date_added, release_year, duration, Year, Age, IMDb, Rotten_Tomatoes):
        self.movie_id = movie_id
        self.type = type
        self.title = title
        self.country = country
        self.date_added = date_added
        self.release_year = release_year
        self.duration = duration
        self.Year = Year
        self.Age = Age
        self.IMDb = IMDb
        self.Rotten_Tomatoes = Rotten_Tomatoes

    def __repr__(self):
        return f"<Movie {self.title}>"

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'type': self.type,
            'title': self.title,
            'country': self.country,
            'date_added': self.date_added,
            'release_year': self.release_year,
            'duration': self.duration,
            'Year': self.Year,
            'Age': self.Age,
            'IMDb': self.IMDb,
            'Rotten_Tomatoes': self.Rotten_Tomatoes
        }
    
class MovieTVShowsFrequency:
    def __init__(self, movie_id, type, title, country, date_added, release_year, duration, Year, Age, IMDb, Rotten_Tomatoes, frequency):
        self.movie_id = movie_id
        self.type = type
        self.title = title
        self.country = country
        self.date_added = date_added
        self.release_year = release_year
        self.duration = duration
        self.Year = Year
        self.Age = Age
        self.IMDb = IMDb
        self.Rotten_Tomatoes = Rotten_Tomatoes
        self.frequency = frequency

    def __repr__(self):
        return f"<Movie {self.title}>"

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'type': self.type,
            'title': self.title,
            'country': self.country,
            'date_added': self.date_added,
            'release_year': self.release_year,
            'duration': self.duration,
            'Year': self.Year,
            'Age': self.Age,
            'IMDb': self.IMDb,
            'Rotten_Tomatoes': self.Rotten_Tomatoes,
            'frequency': self.frequency
        }


class MovieUser:
    def __init__(self, username, password, user_description, user_attributes, num_of_followers):
        self.username = username
        self.password = password
        self.user_description = user_description
        self.user_attributes = user_attributes
        self.num_of_followers = num_of_followers

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        """
        Serialize the User object to a dictionary.
        """
        return {
            'username': self.username,
            'password': self.password,  # Caution: Exposing passwords like this can be a security risk
            'user_description': self.user_description,
            'user_attributes': self.user_attributes,
            'num_of_followers': self.num_of_followers
        }
