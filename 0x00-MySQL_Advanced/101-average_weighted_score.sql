-- creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE projects_weight_total INT;
    DECLARE student_weighted_average FLOAT;
    DECLARE done BOOLEAN DEFAULT FALSE;
    -- declare cursor
    DECLARE cur CURSOR FOR SELECT id FROM users;
    -- declare not found handler
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    SELECT SUM(weight) INTO projects_weight_total FROM projects;

    OPEN cur;

    my_loop:
    LOOP

    -- read the values from the next row that is available in the cursor
    --  FETCH NEXT FROM cur INTO user_id;
        FETCH cur INTO user_id;

    -- read values from next row that is available in the cursor
        IF done THEN
            LEAVE my_loop;
        ELSE
            SELECT SUM((weight * score) / projects_weight_total) INTO student_weighted_average
            FROM projects JOIN corrections
            ON projects.id = corrections.project_id WHERE corrections.user_id = user_id;

            UPDATE users SET average_score = student_weighted_average
            WHERE id = user_id;
        END IF;
    END LOOP;

END $$
DELIMITER ;
