DROP PROCEDURE IF EXISTS InsertDummy;
CREATE PROCEDURE InsertDummy()
BEGIN
    INSERT INTO University (UniversityID, UniversityName, Location, ContactEmail)
    VALUES
        (1, 'Tech University', '123 University Blvd, Tech City', 'contact@techuniversity.edu');

    INSERT INTO Department (DepartmentID, DepartmentName)
    VALUES 
        (1, 'Computer Science'),
        (2, 'Mathematics'),
        (3, 'Physics');

    INSERT INTO Course (CourseID, CreditHours, DepartmentID)
    VALUES
        (101, 3, 1),
        (102, 4, 1),
        (103, 3, 1),
        (201, 3, 2),
        (202, 4, 2),
        (203, 3, 2),
        (301, 3, 3),
        (302, 4, 3),
        (303, 3, 3),
        (104, 3, 1),
        (105, 3, 1),
        (204, 3, 2),
        (205, 4, 2),
        (304, 3, 3),
        (305, 4, 3);

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

    INSERT INTO ClassSection (SectionID, CourseID, StaffID, Seat)
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
END;
