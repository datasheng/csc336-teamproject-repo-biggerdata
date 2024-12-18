-- Create the Class table first
CREATE TABLE IF NOT EXISTS Class (
    SectionID INT PRIMARY KEY,
    CourseID INT,
    StaffID INT,
    Seats INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (StaffID) REFERENCES Staff(Staff_ID)
);

-- Now proceed with other tables that reference Class
CREATE TABLE IF NOT EXISTS account (
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS University (
    UniversityID INT,
    UniversityName VARCHAR(255) UNIQUE,
    Location VARCHAR(255),
    ContactEmail VARCHAR(255),
    PRIMARY KEY (UniversityID)
);

CREATE TABLE IF NOT EXISTS Revenue (
    RevenueID INT,
    UniversityID INT,
    ContractingFee DECIMAL(10, 2),
    PaymentDate DATE,
    PRIMARY KEY (RevenueID),
    FOREIGN KEY (UniversityID) REFERENCES University(UniversityID)
);

CREATE TABLE IF NOT EXISTS Department (
    DepartmentID INT,
    DepartmentName VARCHAR(255) UNIQUE,
    PRIMARY KEY (DepartmentID)
);

CREATE TABLE IF NOT EXISTS Course (
    CourseID INT,
    CourseName VARCHAR(255),
    CreditHours INT,
    DepartmentID INT,
    PRIMARY KEY (CourseID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE IF NOT EXISTS Staff (
    Staff_ID INT,
    Email_ID VARCHAR(255) UNIQUE,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    PRIMARY KEY (Staff_ID)
);

CREATE TABLE IF NOT EXISTS Student (
    UserID INT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    UserEmail VARCHAR(255) UNIQUE,
    PRIMARY KEY (UserID)
);

CREATE TABLE IF NOT EXISTS CoursePrerequisites (
    CourseID INT,
    PrerequisiteID INT,
    PRIMARY KEY (CourseID, PrerequisiteID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (PrerequisiteID) REFERENCES Course(CourseID)
);

CREATE TABLE IF NOT EXISTS ClassSchedule (
    SectionID INT,
    DayOfWeek VARCHAR(10),
    StartTime TIME,
    EndTime TIME,
    PRIMARY KEY (SectionID, DayOfWeek, StartTime),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

CREATE TABLE IF NOT EXISTS StudentCourses (
    UserID INT,
    CourseID INT,
    PRIMARY KEY (UserID, CourseID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE IF NOT EXISTS StudentSchedule (
    UserID INT,
    SectionID INT,
    PRIMARY KEY (UserID, SectionID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

CREATE TABLE IF NOT EXISTS Enrollment (
    RegistrationID INT,
    UserID INT,
    SectionID INT,
    PRIMARY KEY (RegistrationID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

CREATE TABLE IF NOT EXISTS Status (
    UserID INT,
    SectionID INT,
    Status VARCHAR(20),
    PRIMARY KEY (UserID, SectionID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES Class(SectionID)
);

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