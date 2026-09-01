DROP DATABASE IF EXISTS bmi_calculator;

CREATE DATABASE bmi_calculator;

USE bmi_calculator;

-- 1. Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    age INT,
    gender ENUM('male', 'female', 'other') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Indexing for faster lookups on email
    INDEX idx_users_email (email)
);

-- 2. BMI Records Table
CREATE TABLE bmi_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    height DECIMAL(5, 2) NOT NULL,
    height_unit ENUM('cm', 'm') NOT NULL,
    weight DECIMAL(5, 2) NOT NULL,
    weight_unit ENUM('kg', 'lb') NOT NULL,
    bmi DECIMAL(5, 2) NOT NULL,
    bmi_category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Indexing for faster lookups on user_id
    INDEX idx_records_user_id (user_id),
    -- Foreign Key Constraint
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Schema Documentation (Conceptual Verification)
-- To verify the schema structure, you can run:
-- DESCRIBE users;
-- DESCRIBE bmi_records;

-- Relationship Verification:
-- The relationship is established via the foreign key (user_id) in bmi_records
-- referencing the primary key (id) in users. This ensures that every BMI record
-- belongs to a valid user.

-- Verification Steps:
-- 1. Verify Database: mysql -u [user] -p -e "SHOW DATABASES;" (Check for bmi_calculator)
-- 2. Verify Tables: USE bmi_calculator; SHOW TABLES; (Check for users and bmi_records)
-- 3. Verify Relationship: SHOW CREATE TABLE bmi_records; (Check for FOREIGN KEY constraint)
-- 4. Show Schema: DESCRIBE users; DESCRIBE bmi_records; (Check columns, types, and constraints)