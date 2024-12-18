-- Create University table
CREATE TABLE University (
    UniversityID INT PRIMARY KEY,
    UniversityName VARCHAR(255) UNIQUE,
    Location VARCHAR(255),
    ContactEmail VARCHAR(255)
);


CREATE TABLE Revenue (
    RevenueID INT PRIMARY KEY,
    UniversityID INT,
    ContractingFee DECIMAL(10, 2),
    PaymentDate DATE,
    FOREIGN KEY (UniversityID) REFERENCES University(UniversityID)
);

CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(255) UNIQUE
);

-- UPDATED Included CourseName
CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(255),
    CreditHours INT,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- UPDATED Included Professor Name
CREATE TABLE Staff (
    Staff_ID INT PRIMARY KEY,
    Email_ID VARCHAR(255) UNIQUE
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
);


CREATE TABLE Class (
    SectionID INT PRIMARY KEY,
    CourseID INT,
    StaffID INT,
    Seats INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (StaffID) REFERENCES Staff(Staff_ID)
);

--UPDATED included First & Lasnt Name
CREATE TABLE Student (
    UserID INT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    UserEmail VARCHAR(255) UNIQUE
);

CREATE TABLE CoursePrerequisites (
    CourseID INT,
    PrerequisiteID INT,
    PRIMARY KEY (CourseID, PrerequisiteID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (PrerequisiteID) REFERENCES Course(CourseID)
);

CREATE TABLE ClassSchedule (
    SectionID INT,
    DayOfWeek VARCHAR(10),
    StartTime TIME,
    EndTime TIME,
    PRIMARY KEY (SectionID, DayOfWeek, StartTime),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

CREATE TABLE StudentCourses (
    UserID INT,
    CourseID INT,
    PRIMARY KEY (UserID, CourseID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE StudentSchedule (
    UserID INT,
    SectionID INT,
    PRIMARY KEY (UserID, SectionID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

CREATE TABLE Enrollment (
    RegistrationID INT PRIMARY KEY,
    UserID INT,
    SectionID INT,
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

CREATE TABLE Status (
    UserID INT,
    SectionID INT,
    Status VARCHAR(20),
    PRIMARY KEY (UserID, SectionID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

--UPDATE Table for how to calculate revenue for a university
CREATE TABLE RevenueStream (
    UniversityID INT PRIMARY KEY,
    UniversityName VARCHAR(255) NOT NULL,
    StudentCount INT NOT NULL,
    NumClasses INT NOT NULL,
    BaseFee DECIMAL(10, 2) DEFAULT 9000.00 NOT NULL,
    StudentFee DECIMAL(10, 2) GENERATED ALWAYS AS (StudentCount * 0.25) STORED,
    ClassFee DECIMAL(10, 2) GENERATED ALWAYS AS (NumClasses * 4.25) STORED,
    TotalFee DECIMAL(10, 2) GENERATED ALWAYS AS (BaseFee + StudentFee + ClassFee) STORED
);

-- Insert a university
INSERT INTO University (UniversityID, UniversityName, Location, ContactEmail)
VALUES
    (1, 'Tech University', '123 University Blvd, Tech City', 'contact@techuniversity.edu');


INSERT INTO Department (DepartmentID, DepartmentName)
VALUES
    (1, 'Computer Science'),
    (2, 'Mathematics'),
    (3, 'Physics');

-- UPDATED dummy data now has course names
INSERT INTO Course (CourseID, CourseName, CreditHours, DepartmentID)
VALUES
    (101, 'Intro to CS', 3, 1),
    (102, 'Data Structures', 4, 1),
    (103, 'Algorithms', 3, 1),
    (201, 'Calculus I', 3, 2),
    (202, 'Linear Algebra', 4, 2),
    (203, 'Discrete Math', 3, 2),
    (301, 'Mechanics', 3, 3),
    (302, 'Electromagnetism', 4, 3),
    (303, 'Quantum Mechanics', 3, 3),
    (104, 'Computer Organization', 3, 1),
    (105, 'Operating Systems', 3, 1),
    (204, 'Calculus II', 3, 2),
    (205, 'Differential Equations', 4, 2),
    (304, 'Thermodynamics', 3, 3),
    (305, 'Astrophysics', 4, 3);

-- UPDATED Professors now have first & last names
INSERT INTO Staff (StaffID, FirstName, LastName, EmailID)
VALUES
    (1, 'John', 'Doe', 'john.doe@techuniversity.edu'),
    (2, 'Jane', 'Smith', 'jane.smith@techuniversity.edu'),
    (3, 'Emily', 'White', 'emily.white@techuniversity.edu'),
    (4, 'Michael', 'Brown', 'michael.brown@techuniversity.edu'),
    (5, 'Sarah', 'Taylor', 'sarah.taylor@techuniversity.edu'),
    (6, 'David', 'Lee', 'david.lee@techuniversity.edu'),
    (7, 'Alice', 'Wilson', 'alice.wilson@techuniversity.edu'),
    (8, 'Robert', 'Harris', 'robert.harris@techuniversity.edu');

-- Insert classes
INSERT INTO Class (SectionID, CourseID, StaffID, Seats)
VALUES
    (1, 101, 1, 30),
    (2, 102, 2, 25),
    (3, 103, 3, 35),
    (4, 201, 4, 20),
    (5, 202, 5, 25),
    (6, 203, 6, 30),
    (7, 301, 7, 30),
    (8, 302, 8, 25),
    (9, 303, 1, 20),
    (10, 104, 2, 30),
    (11, 105, 3, 25),
    (12, 204, 4, 20),
    (13, 205, 5, 25),
    (14, 304, 6, 30),
    (15, 305, 7, 25);

-- Insert class schedules
INSERT INTO ClassSchedule (SectionID, DayOfWeek, StartTime, EndTime)
VALUES
    (1, 'Monday', '09:00', '10:15'),
    (2, 'Tuesday', '10:30', '11:45'),
    (3, 'Wednesday', '12:00', '13:15'),
    (4, 'Thursday', '13:30', '14:45'),
    (5, 'Friday', '15:00', '16:15'),
    (6, 'Monday', '16:30', '17:45'),
    (7, 'Tuesday', '09:00', '10:15'),
    (8, 'Wednesday', '10:30', '11:45'),
    (9, 'Thursday', '12:00', '13:15'),
    (10, 'Friday', '13:30', '14:45'),
    (11, 'Monday', '15:00', '16:15'),
    (12, 'Tuesday', '16:30', '17:45'),
    (13, 'Wednesday', '09:00', '10:15'),
    (14, 'Thursday', '10:30', '11:45'),
    (15, 'Friday', '12:00', '13:15');

-- Insert revenue stream for Tech University
INSERT INTO RevenueStream (UniversityID, UniversityName, StudentCount, NumClasses)
VALUES
    (1, 'Tech University', 5000, 2000);
