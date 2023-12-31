from flask import Flask, request, jsonify, redirect, url_for, render_template, json
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import mysql.connector
from utils import  AppUser, MovieTVShows

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

db_config = {
    'host': 'cinefusion-central-mysql',  # If Flask isn't running in a Docker container, use Docker's IP here
    # 'host': 'localhost',
    'port': 3306,
    'database': 'movie_db',
    'user': 'root',
    'password': 'rootpassword'
}

@app.route('/')
def home():
    return render_template('login.html')

# Sign-up Route
@app.route('/signupPage')
def signupPage():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get user data from request
    user_data = request.form
    username = user_data['username']
    password = user_data['password']  # In real-world applications, ensure you hash passwords

    # Insert user data into the database
    query = "INSERT INTO User (Username, password, num_of_followers) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, 0))
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()

    return redirect(url_for('home'))


login_manager = LoginManager()
login_manager.init_app(app)

# User model for demonstration
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/current_user')
@login_required
def current_user_route():
    return f"Current user: {current_user.id}"

@app.route('/login', methods=['POST'])
def login():
    user_data = request.form
    username = user_data['username']
    password = user_data['password']

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User WHERE Username = %s and password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user :
        print("user found")
        user = User(username)
        login_user(user)
        return redirect(url_for('homepage'))
    else:
        print("user not found")
        return jsonify({'error': 'Invalid username or password'}), 401

# Example logout route
@app.route('/logout')
def logout():
    logout_user()
    return "You have been logged out"

@app.route('/user/friend')
@login_required
def list_friend():
    # Connect to your MySQL database
    if current_user.is_authenticated:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = """
            SELECT F.username2
            FROM Friend F
            WHERE F.username1 = %s
            UNION
            SELECT F.username1
            FROM Friend F
            WHERE F.username2 = %s;
        """
        cursor.execute(sql, (current_user.id, current_user.id,))
        friends = cursor.fetchall()
        cursor.close()
        conn.close()
        friend_list = []

        for friend in friends:
            friend_list.append(AppUser(*friend))

        return render_template('friend.html', friends=friend_list)


@app.route('/user/add-friend', methods=['POST'])
@login_required
def add_friend():
    user_data = request.form
    username = user_data['username']
    response = {}
    if current_user.is_authenticated:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            # Check if the friendship already exists
            sql = "SELECT * FROM Friend WHERE username1 = %s and username2 = %s"
            cursor.execute(sql, (current_user.id, username,))
            friend = cursor.fetchone()

            if friend:
                response['message'] = 'Friendship already exists.'
            else:
                sql = """
                    INSERT INTO Friend(username1, username2) VALUES(%s, %s);
                """
                cursor.execute(sql, (current_user.id, username,))
                conn.commit()
                response['message'] = 'Friend added successfully.'
        except mysql.connector.Error as err:
            response['error'] = str(err)
        finally:
            cursor.close()
            conn.close()
    else:
        response['error'] = 'User is not authenticated.'
    return redirect(url_for('list_friend'))

@app.route('/watchlist/add-movie', methods=['POST'])
@login_required
def add_watchlist():
    movie_title = request.json['movie_title']
    response = {}

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
        # Check if the movie already added
    sql = "SELECT * FROM Watchlist WHERE Username = %s and title = %s"
    cursor.execute(sql, (current_user.id, movie_title,))
    movie = cursor.fetchone()

    if movie:
        response['message'] = 'Movie already added.'
    else:
        sql = "SELECT movie_id FROM Movie WHERE title = %s"
        cursor.execute(sql, (movie_title,))
        movie_id = cursor.fetchone()
            

        sql = """
                INSERT INTO Watchlist(Username, title, movie_id) VALUES(%s, %s, %s);
            """
        cursor.execute(sql, (current_user.id, movie_title, movie_id[0]))
        conn.commit()
        response['message'] = 'Movie added successfully.'
        cursor.close()
        conn.close()
    return jsonify(response)


def get_movie(movie_name):
    conn = mysql.connector.connect(
        **db_config
    )
    cursor = conn.cursor()
    query = """SELECT Movie.movie_id, Movie.type, Movie.title, Movie.country, 
                Movie.date_added, Movie.release_year, Movie.duration, 
                TvShows.Year, TvShows.Age, TvShows.IMDb, TvShows.`Rotten Tomatoes`
        FROM Movie 
        JOIN TvShows ON Movie.title = TvShows.title
        WHERE Movie.title LIKE %s;"""
    like_pattern = f'%{movie_name}%'
    cursor.execute(query, (like_pattern,))
    movies = cursor.fetchall()
    return movies

def get_movie_by_title(movie_name):
    conn = mysql.connector.connect(
        **db_config
    )
    cursor = conn.cursor()
    query = """SELECT Movie.movie_id, Movie.type, Movie.title, Movie.country, 
                Movie.date_added, Movie.release_year, Movie.duration, 
                TvShows.Year, TvShows.Age, TvShows.IMDb, TvShows.`Rotten Tomatoes`
        FROM Movie 
        JOIN TvShows ON Movie.title = TvShows.title
        WHERE Movie.title = %s;"""
    cursor.execute(query, (movie_name,))
    movie = cursor.fetchone()
    return MovieTVShows(*movie)

@app.route('/watchlistpage')
@login_required
def watchlistpage():
    return render_template('watchlist.html')
@app.route('/user/my-watchlist')
@login_required
def my_watchlist():
    conn = mysql.connector.connect(
        **db_config
    )
    cursor = conn.cursor()
    query = "SELECT title FROM Watchlist WHERE Username = %s"
    cursor.execute(query, (current_user.id,))
    movie_names = cursor.fetchall()
    cursor.close()
    conn.close()
    movies = []
    for movie_name in movie_names:
        movies.append(get_movie_by_title(movie_name[0]))
    movies = [movie.to_dict() for movie in movies]
    return jsonify(movies)
  
@app.route('/movie/list')
def movie_list():
    movie_name = request.args.get('name', default='', type=str)
    movies = get_movie(movie_name)
    movies_list = [MovieTVShows(*movie).to_dict() for movie in movies]
    return jsonify(movies_list)

@app.route('/movie/recommend-by-friend')
@login_required
def recommend_by_friend():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = """
        WITH FriendMovies AS (
            SELECT W.title, COUNT(*) AS frequency
            FROM Watchlist W
            WHERE W.Username IN (
                SELECT F.username2
                FROM Friend F
                WHERE F.username1 = %s
            )
            GROUP BY W.title
        )

        ,
        Top20Movies AS (
            SELECT FM.title, FM.frequency
            FROM FriendMovies FM
            ORDER BY FM.frequency DESC
            LIMIT 20
        )

        SELECT title, frequency
        FROM Top20Movies
        ORDER BY RAND()
        LIMIT 5;
    """
    cursor.execute(sql, (current_user.id,))
    movies= cursor.fetchall()
    cursor.close()
    conn.close()
    movie_list = []
    for movie_name in movies:
        movie_list.append(get_movie_by_title(movie_name[0]))
    return jsonify([movie.to_dict() for movie in movie_list])
    

@app.route('/movie/recommend-by-genre')
@login_required
def recommend_by_genre():
    # Connect to your MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = """
            WITH UserFavoriteGenre AS (
    SELECT gi.genre, COUNT(gi.genre) AS genre_count
    FROM Watchlist w
    JOIN GenreIn gi ON w.movie_id = gi.movie_id
    WHERE w.Username = %s
    GROUP BY gi.genre
    ORDER BY genre_count DESC
    LIMIT 1
),

Top20Movies AS (
    SELECT DISTINCT m.title, pr.rating, pr.platform_name
    FROM Movie m
    INNER JOIN PlatformRating pr ON m.title = pr.title
    INNER JOIN GenreIn gi ON m.movie_id = gi.movie_id
    WHERE gi.genre = (SELECT genre FROM UserFavoriteGenre)
    AND (m.title, pr.rating) IN (
        SELECT title, MAX(rating) AS max_rating
        FROM PlatformRating
        GROUP BY title
    )
    ORDER BY pr.rating DESC
    LIMIT 20
)

SELECT title, rating, platform_name
FROM Top20Movies
ORDER BY RAND()
LIMIT 5;

    """
    cursor.execute(sql, (current_user.id,))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    movie_list = []
    for movie_name in movies:
        movie_list.append(get_movie_by_title(movie_name[0]))
    return jsonify([movie.to_dict() for movie in movie_list])

@app.route('/homepage')
def homepage():
    return render_template('home.html')
    

if __name__ == "__main__":
    app.run(debug=True)
