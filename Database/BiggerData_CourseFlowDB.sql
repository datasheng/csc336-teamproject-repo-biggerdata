-- Create University table
CREATE TABLE University (
    UniversityID INT PRIMARY KEY,
    UniversityName VARCHAR(255) UNIQUE,
    Location VARCHAR(255),
    ContactEmail VARCHAR(255)
);

-- Create Revenue table
CREATE TABLE Revenue (
    RevenueID INT PRIMARY KEY,
    UniversityID INT,
    ContractingFee DECIMAL(10, 2),
    PaymentDate DATE,
    FOREIGN KEY (UniversityID) REFERENCES University(UniversityID)
);

-- Create Department table first
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(255) UNIQUE
);

-- Create other tables after Department
CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CreditHours INT,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE Staff (
    Staff_ID INT PRIMARY KEY,
    Email_ID VARCHAR(255) UNIQUE
);

CREATE TABLE Class (
    SectionID INT PRIMARY KEY,
    CourseID INT,
    StaffID INT,
    Seats INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (StaffID) REFERENCES Staff(Staff_ID)
);

CREATE TABLE Student (
    UserID INT PRIMARY KEY,
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
    DayOfWeek VARCHAR(10), -- e.g., 'Monday', 'Tuesday'
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
    Status VARCHAR(20), -- e.g., 'Enrolled', 'Waitlist', 'Dropped', 'Withdrawn'
    PRIMARY KEY (UserID, SectionID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

-- Insert a university
INSERT INTO University (UniversityID, UniversityName, Location, ContactEmail)
VALUES
    (1, 'Tech University', '123 University Blvd, Tech City', 'contact@techuniversity.edu');

-- Insert departments
INSERT INTO Department (DepartmentID, DepartmentName)
VALUES
    (1, 'Computer Science'),
    (2, 'Mathematics'),
    (3, 'Physics');

-- Insert courses
INSERT INTO Course (CourseID, CreditHours, DepartmentID)
VALUES
    (101, 3, 1), -- CS
    (102, 4, 1),
    (103, 3, 1),
    (201, 3, 2), -- Math
    (202, 4, 2),
    (203, 3, 2),
    (301, 3, 3), -- Physics
    (302, 4, 3),
    (303, 3, 3),
    (104, 3, 1), -- CS
    (105, 3, 1),
    (204, 3, 2), -- Math
    (205, 4, 2),
    (304, 3, 3), -- Physics
    (305, 4, 3);

-- Insert professors
INSERT INTO Staff (Staff_ID, Email_ID)
VALUES
    (1, 'prof1@techuniversity.edu'),
    (2, 'prof2@techuniversity.edu'),
    (3, 'prof3@techuniversity.edu'),
    (4, 'prof4@techuniversity.edu'),
    (5, 'prof5@techuniversity.edu'),
    (6, 'prof6@techuniversity.edu'),
    (7, 'prof7@techuniversity.edu'),
    (8, 'prof8@techuniversity.edu');

-- Insert classes with varying schedules
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

-- Insert class schedules with varying times and days
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
