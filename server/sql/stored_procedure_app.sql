DROP PROCEDURE IF EXISTS RegisterUser;
CREATE PROCEDURE RegisterUser(
	IN firstName VARCHAR(50),
	IN lastName VARCHAR(50),
    IN email VARCHAR(255),
    IN password VARCHAR(255))
BEGIN
    INSERT INTO account (firstName, lastName, email, password)
    VALUES (firstName, lastName, email, password);
END;

DROP PROCEDURE IF EXISTS CheckEmail;
CREATE PROCEDURE CheckEmail(IN email VARCHAR(255))
BEGIN
    SELECT * FROM account WHERE email = email;
END;
