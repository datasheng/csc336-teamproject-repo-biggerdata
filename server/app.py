from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import MySQLdb
from datetime import timedelta


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
            return jsonify({'id': user['id'], 'firstName': user['firstName'], 'lastName': user['lastName'], 'email': user['email']}), 200
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
    courseName = data.get('courseName')  # Make sure to include courseName
    creditHours = data.get('creditHours')
    departmentID = data.get('departmentID')
    
    if not courseID or not courseName or not creditHours or not departmentID:
        return jsonify({'error': 'CourseID, CourseName, CreditHours, and DepartmentID are required'}), 400
    
    cursor = mysql.connection.cursor()
    try:
        # Insert the course into the Course table, including CourseName
        cursor.execute('''
            INSERT INTO Course (CourseID, CourseName, CreditHours, DepartmentID) 
            VALUES (%s, %s, %s, %s)
        ''', (courseID, courseName, creditHours, departmentID))
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
    try:
        # Fetch all departments from the Department table
        cursor.execute('SELECT * FROM Department')
        departments = cursor.fetchall()
        cursor.close()

        if not departments:
            return jsonify({"error": "No departments found"}), 404

        return jsonify({'departments': departments}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/register_student', methods=['POST'])
def register_student():
    data = request.get_json()
    user_id = data.get('UserID')
    section_id = data.get('SectionID')

    # Validate input
    if not user_id or not section_id:
        return jsonify({"error": "UserID and SectionID are required fields"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check for duplicate entry in StudentSchedule (i.e., student is already enrolled in this section)
        cursor.execute(
            'SELECT * FROM StudentSchedule WHERE UserID = %s AND SectionID = %s',
            (user_id, section_id)
        )
        existing_entry = cursor.fetchone()
        if existing_entry:
            return jsonify({"error": "Student is already registered for this section"}), 400

        # Insert data into StudentSchedule table
        cursor.execute(
            'INSERT INTO StudentSchedule (UserID, SectionID) VALUES (%s, %s)',
            (user_id, section_id)
        )

        # Now, insert the default status into the Status table
        cursor.execute(
            'INSERT INTO Status (UserID, SectionID, Status) VALUES (%s, %s, %s)',
            (user_id, section_id, 'Enrolled')  # Default status is "Enrolled"
        )

        mysql.connection.commit()

        return jsonify({'message': f'Student {user_id} successfully registered for Section {section_id}!'}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()


@app.route('/api/add-student', methods=['POST'])
def add_student():
    data = request.get_json()
    user_id = data.get('UserID')
    first_name = data.get('firstName')
    last_name = data.get('lastName')

    # Validate input
    if not first_name or not last_name or not user_id:
        return jsonify({"error": "UserID, firstName, and lastName are required fields"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Insert data into the Student table, without using the Email field
        cursor.execute('''
            INSERT INTO Student (UserID, FirstName, LastName)
            VALUES (%s, %s, %s)
        ''', (user_id, first_name, last_name))
        mysql.connection.commit()

        return jsonify({"message": f"Student {first_name} {last_name} added successfully!", "UserID": user_id}), 200
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
            SELECT s.UserID, s.FirstName, s.LastName, s.UserEmail 
            FROM Student s 
            JOIN StudentCourses sc ON s.UserID = sc.UserID 
            WHERE sc.CourseID = %s
            ''',
            (course_id,)
        )
        students = cursor.fetchall()
        return jsonify({'courseID': course_id, 'students': students}), 200
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
    if not section_id or not course_id or seats is None or not staff_id:
        return jsonify({"error": "SectionID, CourseID, StaffID, and Seats are required fields"}), 400

    cursor = mysql.connection.cursor()
    
    try:
        # Check if the StaffID exists in the Staff table
        cursor.execute('SELECT * FROM Staff WHERE Staff_ID = %s', (staff_id,))
        staff = cursor.fetchone()
        if not staff:
            return jsonify({"error": f"Staff with StaffID {staff_id} does not exist"}), 404

        # Check if the SectionID already exists in the Class table
        cursor.execute('SELECT * FROM Class WHERE SectionID = %s', (section_id,))
        existing_class = cursor.fetchone()
        if existing_class:
            return jsonify({"error": f"Class Section with SectionID {section_id} already exists"}), 400

        # Check if the course exists in the Course table
        cursor.execute('SELECT * FROM Course WHERE CourseID = %s', (course_id,))
        course = cursor.fetchone()
        if not course:
            return jsonify({"error": f"Course with CourseID {course_id} does not exist"}), 404

        # Insert the new class into the Class table
        cursor.execute('''
            INSERT INTO Class (SectionID, CourseID, StaffID, Seats)
            VALUES (%s, %s, %s, %s)
        ''', (section_id, course_id, staff_id, seats))

        mysql.connection.commit()

        return jsonify({"message": f"Class Section {section_id} added successfully!"}), 200

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
        # Check if the status exists for the student in the specific section
        cursor.execute('''
            SELECT Status
            FROM Status
            WHERE UserID = %s AND SectionID = %s
        ''', (user_id, section_id))

        # Fetch the status from the Status table
        status_entry = cursor.fetchone()

        if not status_entry:
            return jsonify({"error": f"No status found for Student {user_id} in Section {section_id}"}), 404

        # Return the status
        return jsonify({
            "UserID": user_id,
            "SectionID": section_id,
            "Status": status_entry['Status']
        }), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()



@app.route('/api/add-department', methods=['POST'])
def add_department():
    data = request.get_json()
    department_id = data.get('DepartmentID')
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

        # Format StartTime and EndTime as strings (e.g., "HH:MM:SS")
        formatted_schedule = []
        for item in schedule:
            start_time = None
            end_time = None

            if item['StartTime']:
                # If StartTime is a timedelta, convert to "HH:MM:SS"
                if isinstance(item['StartTime'], timedelta):
                    start_time = str(item['StartTime'])
                else:
                    start_time = item['StartTime'].strftime('%H:%M:%S')

            if item['EndTime']:
                # If EndTime is a timedelta, convert to "HH:MM:SS"
                if isinstance(item['EndTime'], timedelta):
                    end_time = str(item['EndTime'])
                else:
                    end_time = item['EndTime'].strftime('%H:%M:%S')

            formatted_schedule.append({
                'SectionID': item['SectionID'],
                'CourseID': item['CourseID'],
                'DayOfWeek': item['DayOfWeek'],
                'StartTime': start_time,
                'EndTime': end_time
            })

        # Return the schedule as a JSON response
        return jsonify({'UserID': user_id, 'Schedule': formatted_schedule}), 200

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
        # Check if the student exists in the Student table
        cursor.execute('SELECT * FROM Student WHERE UserID = %s', (user_id,))
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": f"Student with UserID {user_id} does not exist"}), 404

        # Check if the section exists in the Class table
        cursor.execute('SELECT * FROM Class WHERE SectionID = %s', (section_id,))
        section = cursor.fetchone()
        if not section:
            return jsonify({"error": f"Class Section with SectionID {section_id} does not exist"}), 404

        # Check if the student is already enrolled in the class
        cursor.execute('SELECT * FROM StudentSchedule WHERE UserID = %s AND SectionID = %s', (user_id, section_id))
        existing_schedule = cursor.fetchone()
        if existing_schedule:
            return jsonify({"error": "Student is already enrolled in this section"}), 400

        # Add the class to the student's schedule
        cursor.execute('''
            INSERT INTO StudentSchedule (UserID, SectionID) 
            VALUES (%s, %s)
        ''', (user_id, section_id))
        mysql.connection.commit()
        return jsonify({"message": f"Class Section {section_id} successfully added to the schedule for Student {user_id}!"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/deregister_student', methods=['POST'])
def deregister_student():
    data = request.get_json()
    user_id = data.get('UserID')
    course_id = data.get('CourseID')

    # Validate input
    if not user_id or not course_id:
        return jsonify({"error": "UserID and CourseID are required"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check if the student is enrolled in the course
        cursor.execute('SELECT * FROM StudentCourses WHERE UserID = %s AND CourseID = %s', (user_id, course_id))
        enrollment = cursor.fetchone()
        if not enrollment:
            return jsonify({"error": f"Student {user_id} is not enrolled in Course {course_id}"}), 404

        # Deregister the student from the course
        cursor.execute('DELETE FROM StudentCourses WHERE UserID = %s AND CourseID = %s', (user_id, course_id))
        mysql.connection.commit()

        return jsonify({"message": f"Student {user_id} successfully deregistered from Course {course_id}!"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/get-student-profile', methods=['GET'])
def get_student_profile():
    if 'email' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Student WHERE UserEmail = %s', (session['email'],))
        student = cursor.fetchone()
        cursor.close()
        if student:
            return jsonify({
                'UserID': student['UserID'],
                'UserEmail': student['UserEmail'],
                'Name': student['FirstName'] + ' ' + student['LastName'],
            }), 200
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'message': 'Unauthorized access'}), 401

@app.route('/api/get-course-details', methods=['POST'])
def get_course_details():
    data = request.get_json()
    course_id = data.get('CourseID')

    # Validate input
    if not course_id:
        return jsonify({"error": "CourseID is a required field"}), 400

    cursor = mysql.connection.cursor()
    try:
        # Check if the course exists and fetch details, including CourseName
        cursor.execute('SELECT * FROM Course WHERE CourseID = %s', (course_id,))
        course = cursor.fetchone()

        if not course:
            return jsonify({"error": f"Course with ID {course_id} not found"}), 404

        # Fetch department details related to the course
        cursor.execute('SELECT DepartmentName FROM Department WHERE DepartmentID = %s', (course['DepartmentID'],))
        department = cursor.fetchone()

        if not department:
            return jsonify({"error": "Department details not found"}), 404

        # Return the course details along with department information
        return jsonify({
            'CourseID': course['CourseID'],
            'CourseName': course['CourseName'],  # Return CourseName
            'CreditHours': course['CreditHours'],
            'DepartmentName': department['DepartmentName']
        }), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()


@app.route('/api/get-staff-schedule', methods=['POST'])
def get_staff_schedule():
    data = request.get_json()
    staff_id = data.get('StaffID')
    
    if not staff_id:
        return jsonify({"error": "StaffID is required"}), 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT * FROM Staff WHERE Staff_ID = %s', (staff_id,))
        staff = cursor.fetchone()
        
        if not staff:
            return jsonify({"error": f"Staff with StaffID {staff_id} does not exist"}), 404

        cursor.execute('''
            SELECT c.SectionID, c.CourseID, cs.DayOfWeek, cs.StartTime, cs.EndTime
            FROM ClassSection c
            JOIN ClassSchedule cs ON c.SectionID = cs.SectionID
            WHERE c.StaffID = %s
        ''', (staff_id,))
        
        schedule = cursor.fetchall()

        return jsonify({'StaffID': staff_id, 'Schedule': schedule}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()


@app.route('/api/get-sections-for-course', methods=['POST'])
def get_sections_for_course():
    data = request.get_json()
    course_id = data.get('CourseID')

    if not course_id:
        return jsonify({"error": "CourseID is required"}), 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('SELECT * FROM Class WHERE CourseID = %s', (course_id,))
        sections = cursor.fetchall()

        if not sections:
            return jsonify({"error": f"No sections found for Course {course_id}"}), 404

        return jsonify({'CourseID': course_id, 'Sections': sections}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()

@app.route('/api/add-staff', methods=['POST'])
def add_staff():
    data = request.get_json()
    staff_id = data.get('StaffID')
    first_name = data.get('FirstName')
    last_name = data.get('LastName')

    # Validate input
    if not staff_id or not first_name or not last_name:
        return jsonify({"error": "StaffID, FirstName, and LastName are required fields"}), 400

    cursor = mysql.connection.cursor()
    
    try:
        # Check if the StaffID already exists
        cursor.execute('SELECT * FROM Staff WHERE Staff_ID = %s', (staff_id,))
        existing_staff = cursor.fetchone()
        if existing_staff:
            return jsonify({"error": f"Staff with StaffID {staff_id} already exists"}), 400

        # Insert the new staff into the Staff table (without Email)
        cursor.execute('''
            INSERT INTO Staff (Staff_ID, FirstName, LastName)
            VALUES (%s, %s, %s)
        ''', (staff_id, first_name, last_name))

        mysql.connection.commit()

        return jsonify({"message": f"Staff {first_name} {last_name} added successfully!"}), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()














if __name__ == '__main__':
    initialize()
    app.run(debug=True)
