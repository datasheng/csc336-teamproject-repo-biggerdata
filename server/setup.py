from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MY_HOST')
app.config['MYSQL_USER'] = os.getenv('MY_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MY_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MY_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS account (firstName VARCHAR(50) NOT NULL, lastName VARCHAR(50) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, PRIMARY KEY (email))')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Department (
            DepartmentID VARCHAR(255) PRIMARY KEY,
            DepartmentName VARCHAR(255) NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS University (
            UniversityID BIGINT PRIMARY KEY AUTO_INCREMENT,
            Enrolled BIGINT
        )
    ''')   
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Course (
        CourseID VARCHAR(255) PRIMARY KEY,
        CreditHours INT NOT NULL,
        DepartmentID VARCHAR(255),
        CollegeID BIGINT,
        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID),
        FOREIGN KEY (CollegeID) REFERENCES University(UniversityID)
    )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            UserID BIGINT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(255) NOT NULL,
            UserEmail VARCHAR(255) NOT NULL UNIQUE,
            UniversityID BIGINT,
            FOREIGN KEY (UniversityID) REFERENCES University(UniversityID)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS StudentCourses (
            UserID BIGINT NOT NULL,
            CourseID VARCHAR(255) NOT NULL,
            PRIMARY KEY (UserID, CourseID),
            FOREIGN KEY (UserID) REFERENCES Student(UserID),
            FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
        )
    ''')
    
    mysql.connection.commit()
    cursor.close()
    return 'table created'

if __name__ == '__main__':
    app.run(debug=True)
