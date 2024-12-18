-- Change delimiter to $$ temporarily
DELIMITER $$

-- Drop the RegisterUser procedure if it exists
DROP PROCEDURE IF EXISTS RegisterUser;

-- Create the RegisterUser procedure
CREATE PROCEDURE RegisterUser(
    IN firstNameIn VARCHAR(50),
    IN lastNameIn VARCHAR(50),
    IN emailIn VARCHAR(255),
    IN passwordIn VARCHAR(255))
BEGIN
    INSERT INTO account (firstName, lastName, email, password)
    VALUES (firstNameIn, lastNameIn, emailIn, passwordIn);
END$$

-- Drop the CheckEmail procedure if it exists
DROP PROCEDURE IF EXISTS CheckEmail;

-- Create the CheckEmail procedure
CREATE PROCEDURE CheckEmail(IN emailIn VARCHAR(255))
BEGIN
    SELECT * FROM account WHERE email = emailIn;
END$$

-- Reset delimiter back to default
DELIMITER ;
