-- creates a trigger that resets the attribute valid_email only when the email has been changed.
DELIMITER //
CREATE TRIGGER after_users_update BEFORE UPDATE ON users
FOR EACH ROW
IF OLD.email != NEW.email THEN SET NEW.valid_email = 0;
END IF;
//

DELIMITER ;
