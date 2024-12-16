DROP PROCEDURE IF EXISTS RegisterUser;
CREATE PROCEDURE RegisterUser(
    IN firstNameIn VARCHAR(50),
    IN lastNameIn VARCHAR(50),
    IN emailIn VARCHAR(255),
    IN passwordIn VARCHAR(255))
BEGIN
    INSERT INTO account (firstName, lastName, email, password)
    VALUES (firstNameIn, lastNameIn, emailIn, passwordIn);
END;

DROP PROCEDURE IF EXISTS CheckEmail;
CREATE PROCEDURE CheckEmail(IN emailIn VARCHAR(255))
BEGIN
    SELECT * FROM account WHERE email = emailIn;
END;
