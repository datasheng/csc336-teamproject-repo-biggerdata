from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = os.getenv('MY_HOST')
app.config['MYSQL_USER'] = os.getenv('MY_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MY_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MY_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT DATABASE()')
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name}")
        return 'Connection successful'
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return f"Error: {e}"


def create_table():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS account (
                firstName VARCHAR(50) NOT NULL,
                lastName VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                PRIMARY KEY (email)
            )
        ''')
        mysql.connection.commit()
        cursor.close()
        print("Table 'account' created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == '__main__':
    with app.app_context():
        create_table()

