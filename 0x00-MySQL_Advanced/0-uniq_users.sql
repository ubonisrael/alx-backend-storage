--  creates a table of users on a database
CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTO_INCREMENT, email VARCHAR(255) UNIQUE NOT NULL, name VARCHAR(255));
