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

def stored_procedure():
    cursor = mysql.connection.cursor()
    try:
        with open('sql/stored_procedure_app.sql', 'r') as f:
            sql = f.read()
            cursor.execute(sql)
            mysql.connection.commit()
            print('stored procedure created')
    except Exception as e:
        print(f'stored procedure error: {e}')
    finally:
        if cursor:
            cursor.close()

def initialize():
    with app.app_context():
        stored_procedure()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    hash = generate_password_hash(password)
    cursor = mysql.connection.cursor()
    # check if email already exists
    cursor.callproc('CheckEmail', (email,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return jsonify({'error': 'Email already exists'}), 400
    # if not then register user
    cursor = mysql.connection.cursor()
    cursor.callproc('RegisterUser', (firstName, lastName, email, hash))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    cursor = mysql.connection.cursor()
    # check if email already exists
    cursor.callproc('CheckEmail', (email,))
    user = cursor.fetchone()
    cursor.close()
    # if so and password matches then log in user
    if user and check_password_hash(user['password'], password):
        session['email'] = user['email']
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Wrong email or password'}), 400

@app.route('/api/homepage', methods=['GET'])
def homepage():
    # if user is logged in
    if 'email' in session:
        cursor = mysql.connection.cursor()
        cursor.callproc('CheckEmail', (session['email'],))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return jsonify({'firstName': user['firstName'], 'lastName': user['lastName'], 'email': user['email']}), 200
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
        cursor.execute('SELECT * FROM Course')  # Fetch all courses
        courses = cursor.fetchall()
        cursor.close()

        return jsonify({'courses': courses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_course', methods=['DELETE'])
def delete_course():
    data = request.get_json()
    course_id = data.get('CourseID')

    # Validate that course_id is a number
    if not course_id or not isinstance(course_id, int):
        return jsonify({"error": "CourseID must be a valid integer"}), 400

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


@app.route('/api/list_departments', methods=['GET'])
def list_departments(): 
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

@app.route('/api/add-student', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('Name')
    user_email = data.get('UserEmail')
    university_id = data.get('UniversityID')

    # Validate input
    if not name or not user_email or not university_id:
        return jsonify({"error": "Name, UserEmail, and UniversityID are required fields"}), 400

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

        # Fetch the newly created student ID
        new_student_id = cursor.lastrowid
        return jsonify({"message": f"Student {name} added successfully!", "UserID": new_student_id}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()


@app.route('/api/get-status', methods=['POST'])
def get_status():
    data = request.get_json()
    user_id = data.get('UserID')
    section_id = data.get('SectionID')

    # Validate input
    if not user_id or not section_id:
        return jsonify({"error": "UserID and SectionID are required fields"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check if the user exists
        cursor.execute('SELECT * FROM Student WHERE UserID = %s', (user_id,))
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": f"Student with UserID {user_id} does not exist"}), 404

        # Check if the section exists
        cursor.execute('SELECT * FROM Class WHERE SectionID = %s', (section_id,))
        section = cursor.fetchone()
        if not section:
            return jsonify({"error": f"Class with SectionID {section_id} does not exist"}), 404

        # Fetch the status of the student in the class
        cursor.execute(
            '''
            SELECT Status
            FROM Status
            WHERE UserID = %s AND SectionID = %s
            ''',
            (user_id, section_id)
        )
        status_entry = cursor.fetchone()
        if not status_entry:
            return jsonify({"error": f"No status found for Student {user_id} in Class {section_id}"}), 404

        # Return the status
        return jsonify({"UserID": user_id, "SectionID": section_id, "Status": status_entry['Status']}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/add-class', methods=['POST'])
def add_class():
    data = request.get_json()
    section_id = data.get('SectionID')
    course_id = data.get('CourseID')
    staff_id = data.get('StaffID')
    seats = data.get('Seats')

    # Validate input
    if not section_id or not course_id or seats is None:
        return jsonify({"error": "SectionID, CourseID, and Seats are required fields"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check if the SectionID already exists in ClassSection table
        cursor.execute('SELECT * FROM ClassSection WHERE SectionID = %s', (section_id,))
        existing_class = cursor.fetchone()
        if existing_class:
            return jsonify({"error": f"Class Section with SectionID {section_id} already exists"}), 400

        # Check if the course exists
        cursor.execute('SELECT * FROM Course WHERE CourseID = %s', (course_id,))
        course = cursor.fetchone()
        if not course:
            return jsonify({"error": f"Course with CourseID {course_id} does not exist"}), 404

        # Optional: Check if the staff exists
        if staff_id:
            cursor.execute('SELECT * FROM Staff WHERE Staff_ID = %s', (staff_id,))
            staff = cursor.fetchone()
            if not staff:
                return jsonify({"error": f"Staff with StaffID {staff_id} does not exist"}), 404

        # Insert the class into the ClassSection table
        cursor.execute(
            '''
            INSERT INTO ClassSection (SectionID, CourseID, StaffID, Seats)
            VALUES (%s, %s, %s, %s)
            ''',
            (section_id, course_id, staff_id, seats)
        )
        mysql.connection.commit()
        return jsonify({"message": f"Class Section {section_id} added successfully for Course {course_id}!"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/add-department', methods=['POST'])
def add_department():
    data = request.get_json()
    department_id = data.get('DepartmentID')  # Expecting DepartmentID to be passed
    department_name = data.get('DepartmentName')

    if not department_id or not department_name:
        return jsonify({"error": "DepartmentID and DepartmentName are required"}), 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO Department (DepartmentID, DepartmentName)
            VALUES (%s, %s)
        ''', (department_id, department_name))
        mysql.connection.commit()
        return jsonify({"message": f"Department {department_name} added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()
        
@app.route('/api/get-student-schedule', methods=['POST'])
def get_student_schedule():
    data = request.get_json()  # Receive JSON data in the body
    user_id = data.get('UserID')  # Extract UserID from the JSON body

    # Validate input
    if not user_id:
        return jsonify({"error": "UserID is required"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check if the student exists
        cursor.execute('SELECT * FROM Student WHERE UserID = %s', (user_id,))
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": f"Student with UserID {user_id} does not exist"}), 404

        # Query to fetch courses and schedule the student is enrolled in
        cursor.execute('''
            SELECT c.SectionID, c.CourseID, cs.DayOfWeek, cs.StartTime, cs.EndTime
            FROM StudentSchedule ss
            JOIN Class c ON ss.SectionID = c.SectionID
            JOIN ClassSchedule cs ON c.SectionID = cs.SectionID
            WHERE ss.UserID = %s
        ''', (user_id,))

        schedule = cursor.fetchall()
        if not schedule:
            return jsonify({"message": "No classes found for this student."}), 404

        # Return the schedule as a JSON response
        return jsonify({'UserID': user_id, 'Schedule': schedule}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/add-class-to-schedule', methods=['POST'])
def add_class_to_schedule():
    data = request.get_json()
    user_id = data.get('UserID')
    section_id = data.get('SectionID')

    if not user_id or not section_id:
        return jsonify({"error": "UserID and SectionID are required fields"}), 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT * FROM Student WHERE UserID = %s', (user_id,))
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": f"Student with UserID {user_id} does not exist"}), 404

        cursor.execute('SELECT * FROM ClassSection WHERE SectionID = %s', (section_id,))
        section = cursor.fetchone()
        if not section:
            return jsonify({"error": f"Class Section with SectionID {section_id} does not exist"}), 404

        cursor.execute(
            'SELECT * FROM StudentSchedule WHERE UserID = %s AND SectionID = %s',
            (user_id, section_id)
        )
        existing_entry = cursor.fetchone()
        if existing_entry:
            return jsonify({"error": "Student is already enrolled in this section"}), 400

        cursor.execute(
            'INSERT INTO StudentSchedule (UserID, SectionID) VALUES (%s, %s)',
            (user_id, section_id)
        )
        mysql.connection.commit()
        return jsonify({"message": f"Class Section {section_id} successfully added to the schedule for Student {user_id}!"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()









if __name__ == '__main__':
    initialize()
    app.run(debug=True)
