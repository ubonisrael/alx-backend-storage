-- creates a stored procedure AddBonus that adds a new correction for a student.
DELIMITER $$
CREATE PROCEDURE AddBonus(
    IN user_id VARCHAR(255),
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE projects_id INT;

    SELECT COUNT(*) INTO projects_id FROM projects WHERE name = project_name;

    IF projects_id < 1 THEN
        INSERT INTO projects (name) VALUES (project_name);
    END IF;

    SELECT id INTO projects_id FROM projects WHERE name = project_name;
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, projects_id, score);
END $$
DELIMITER ;
