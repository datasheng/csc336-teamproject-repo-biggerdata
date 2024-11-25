from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = os.getenv('MY_KEY')
app.config['MYSQL_HOST'] = os.getenv('MY_HOST')
app.config['MYSQL_USER'] = os.getenv('MY_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MY_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MY_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    hash = generate_password_hash(password)
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM account WHERE email = %s', (email,))
    user = cursor.fetchone()
    if user:
        cursor.close()
        return jsonify({'error': 'Email already exists'}), 400
    cursor.execute('INSERT INTO account (firstName, lastName, email, password) VALUES (%s, %s, %s, %s)', (firstName, lastName, email, hash))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User registered'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM account WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    if user and check_password_hash(user['password'], password):
        session['isLogin'] = True
        session['email'] = user['email']
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Wrong email or password'}), 400

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    if 'isLogin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE email = %s', (session['email'],))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return jsonify({'firstName': user['firstName'], 'lastName': user['lastName']}), 200
        return jsonify({'error': 'User not found'}), 400
    return jsonify({'message': 'Unauthorized access'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('isLogin', None)
    session.pop('email', None)
    return jsonify({'message': 'Log out successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
