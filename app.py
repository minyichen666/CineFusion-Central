from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    conn = mysql.connector.connect(
        host='localhost',  # If Flask isn't running in a Docker container, use Docker's IP here
        port=3306,
        database='movie_db',
        user='root',
        password='rootpassword'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    current_time = cursor.fetchone()
    cursor.close()
    conn.close()
    return f"Current time in MySQL: {current_time}"

if __name__ == "__main__":
    app.run(debug=True)
