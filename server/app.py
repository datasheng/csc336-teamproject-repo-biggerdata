from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import MySQLdb

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
        session['email'] = user['email']
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Wrong email or password'}), 400

@app.route('/api/homepage', methods=['GET'])
def homepage():
    if 'email' in session:
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
    session.pop('email', None)
    return jsonify({'message': 'Log out successful'}), 200

@app.route('/api/add-course', methods=['POST'])
def add_course():
    data = request.get_json()
    courseID = data.get('courseID')
    creditHours = data.get('creditHours')
    departmentID = data.get('departmentID')
    collegeID = data.get('collegeID')
    
    if not courseID or not creditHours:
        return jsonify({'error': 'CourseID and CreditHours are required'}), 400
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO Course (CourseID, CreditHours, DepartmentID, CollegeID) 
            VALUES (%s, %s, %s, %s)
        ''', (courseID, creditHours, departmentID, collegeID))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Course added successfully'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/list_courses', methods=['GET'])
def list_courses():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM course')  # Fetch all courses
        courses = cursor.fetchall()
        cursor.close()

        # Return the courses as a JSON response
        return jsonify({'courses': courses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_course', methods=['DELETE'])
def delete_course():
    data = request.get_json()
    course_id = data.get('CourseID')

    try:
        cursor = mysql.connection.cursor()
        # Check if the course has related student enrollments
        cursor.execute('SELECT COUNT(*) AS count FROM StudentCourses WHERE CourseID = %s', (course_id,))
        result = cursor.fetchone()

        if result['count'] > 0:
            cursor.close()
            return jsonify({'error': f'Cannot delete Course {course_id} because it has related student enrollments.'}), 400

        # Proceed with deletion if no dependencies exist
        cursor.execute('DELETE FROM Course WHERE CourseID = %s', (course_id,))
        mysql.connection.commit()

        cursor.close()
        return jsonify({'message': f'Course {course_id} deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    data = request.get_json()
    course_id = data.get('CourseID')

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM Course WHERE CourseID = %s', (course_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': f'Course {course_id} deleted successfully!'}), 200

@app.route('/api/list_departments', methods=['GET'])
def list_departments(): 
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Department')
    departments = cursor.fetchall()
    cursor.close()

    return jsonify({'departments': departments}), 200


    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Department')
    departments = cursor.fetchall()
    cursor.close()

    return jsonify({'departments': departments}), 200

@app.route('/api/register_student', methods=['POST'])
def register_student():
    data = request.get_json()
    user_id = data.get('UserID')
    course_id = data.get('CourseID')

    # Validate input
    if not user_id or not course_id:
        return jsonify({"error": "UserID and CourseID are required fields"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check for duplicate entry
        cursor.execute(
            'SELECT * FROM StudentCourses WHERE UserID = %s AND CourseID = %s',
            (user_id, course_id)
        )
        existing_entry = cursor.fetchone()
        if existing_entry:
            return jsonify({"error": "Student is already registered for this course"}), 400

        # Insert data into StudentCourses table
        cursor.execute(
            'INSERT INTO StudentCourses (UserID, CourseID) VALUES (%s, %s)',
            (user_id, course_id)
        )
        mysql.connection.commit()
        return jsonify({'message': f'Student {user_id} registered for course {course_id} successfully!'}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/list_students_in_course', methods=['POST'])
def list_students_in_course():
    data = request.get_json()
    course_id = data.get('CourseID')

    # Validate input
    if not course_id:
        return jsonify({"error": "CourseID is a required field"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check if the course exists
        cursor.execute('SELECT * FROM Course WHERE CourseID = %s', (course_id,))
        course = cursor.fetchone()
        if not course:
            return jsonify({"error": f"Course with ID {course_id} does not exist"}), 404

        # Query to fetch students in the course
        cursor.execute(
            '''
            SELECT s.UserID, s.Name, s.UserEmail 
            FROM Student s 
            JOIN StudentCourses sc ON s.UserID = sc.UserID 
            WHERE sc.CourseID = %s
            ''',
            (course_id,)
        )
        students = cursor.fetchall()
        return jsonify({'courseID': course_id, 'students': students}), 200
    except Exception as e:
        # Handle database query errors
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('Name')
    user_email = data.get('UserEmail')
    university_id = data.get('UniversityID')

    # Validate input
    if not name or not user_email:
        return jsonify({"error": "Name and UserEmail are required fields"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Insert data into the Student table
        cursor.execute(
            '''
            INSERT INTO Student (Name, UserEmail, UniversityID)
            VALUES (%s, %s, %s)
            ''',
            (name, user_email, university_id)
        )
        mysql.connection.commit()
        return jsonify({"message": f"Student {name} added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()
  








if __name__ == '__main__':
    app.run(debug=True)
