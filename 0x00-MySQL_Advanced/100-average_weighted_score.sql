-- creates a stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id VARCHAR(255)
)
BEGIN
    DECLARE projects_weight_total INT;
    DECLARE student_weighted_average FLOAT;

    SELECT SUM(weight) INTO projects_weight_total FROM projects;

    SELECT SUM((weight * score) / projects_weight_total) INTO student_weighted_average
    FROM projects JOIN corrections
    ON projects.id = corrections.project_id WHERE corrections.user_id = user_id;

    UPDATE users SET average_score = student_weighted_average
    WHERE id = user_id;

END $$
DELIMITER ;
