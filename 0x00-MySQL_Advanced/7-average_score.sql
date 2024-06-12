-- creates a stored procedure ComputeAverageScoreForUser that computes
-- and store the average score for a student. Note: An average score
-- can be a decimal
--    DECLARE avg_score FLOAT;
--    SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = user_id;
--    UPDATE users SET average_score = avg_score WHERE id = user_id;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN userId VARCHAR(255)
)
BEGIN

    UPDATE users SET average_score = (
        SELECT AVG(score) FROM corrections WHERE user_id = userId
    ) WHERE id = userId;

END $$
DELIMITER ;
