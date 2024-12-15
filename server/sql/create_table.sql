CREATE TABLE IF NOT EXISTS account (
	firstName VARCHAR(50) NOT NULL,
	lastName VARCHAR(50) NOT NULL,
	email VARCHAR(255),
	password VARCHAR(255) NOT NULL,
	PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS Department (
    DepartmentID INT,
    DepartmentName VARCHAR(255) UNIQUE,
	PRIMARY KEY (DepartmentID)
);

CREATE TABLE IF NOT EXISTS Course (
    CourseID INT,
    Credit INT,
    DepartmentID INT,
	PRIMARY KEY (CourseID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE IF NOT EXISTS Staff (
    StaffID INT,
    StaffEmail VARCHAR(255) UNIQUE,
	PRIMARY KEY (StaffID)
);

CREATE TABLE IF NOT EXISTS ClassSection (
    SectionID INT,
    CourseID INT,
    StaffID INT,
    Seat INT,
	PRIMARY KEY (SectionID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);

CREATE TABLE IF NOT EXISTS Student (
    UserID INT,
    UserEmail VARCHAR(255) UNIQUE,
	PRIMARY KEY (UserID)
);

CREATE TABLE IF NOT EXISTS ClassSchedule (
    SectionID INT,
    DayOfWeek VARCHAR(10),
    StartTime TIME,
    EndTime TIME,
    PRIMARY KEY (SectionID, DayOfWeek, StartTime),
    FOREIGN KEY (SectionID) REFERENCES ClassSection(SectionID)
);

CREATE TABLE IF NOT EXISTS StudentCourse (
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
    FOREIGN KEY (SectionID) REFERENCES ClassSection(SectionID)
);

CREATE TABLE IF NOT EXISTS Enrollment (
    EnrollID INT,
    UserID INT,
    SectionID INT,
	PRIMARY KEY (EnrollID),
    FOREIGN KEY (UserID) REFERENCES Student(UserID),
    FOREIGN KEY (SectionID) REFERENCES ClassSection(SectionID)
);
