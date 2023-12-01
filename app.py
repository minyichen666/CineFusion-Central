from flask import Flask, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

db_config = {
    'host': 'cinefusion-central-mysql',  # If Flask isn't running in a Docker container, use Docker's IP here
    'port': 3306,
    'database': 'movie_db',
    'user': 'root',
    'password': 'rootpassword'
}

@app.route('/')
def index():
    conn = mysql.connector.connect(
        **db_config
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    current_time = cursor.fetchone()
    cursor.close()
    conn.close()
    return f"Current time in MySQL: {current_time}"

# Sign-up Route
@app.route('/signup', methods=['POST'])
def signup():
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get user data from request
    user_data = request.json
    username = user_data['username']
    password = user_data['password']  # In real-world applications, ensure you hash passwords

    # Insert user data into the database
    query = "INSERT INTO User (Username, password, num_of_followers) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, 0))
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()

    return json.dumps({'status': 'success'}), 200


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

# Example login route for demonstration purposes
@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
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

    if user and user['password'] == password:
        user = User(username)
        login_user(user)
        return redirect(url_for('current_user_route'))
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Example logout route
@app.route('/logout')
def logout():
    logout_user()
    return "You have been logged out"

if __name__ == "__main__":
    app.run(debug=True)
