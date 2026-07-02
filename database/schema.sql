CREATE DATABASE IF NOT EXISTS dropout_prediction_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE dropout_prediction_db;

-- ============================================================
-- FACULTY TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE,
    phone VARCHAR(20),
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- STUDENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    register_number VARCHAR(50) UNIQUE,
    name VARCHAR(150) NOT NULL,
    department VARCHAR(100),
    year VARCHAR(20),
    semester VARCHAR(20),
    section VARCHAR(10),
    gender VARCHAR(20),
    dob DATE,
    email VARCHAR(150),
    phone VARCHAR(20),
    parent_name VARCHAR(150),
    parent_phone VARCHAR(20),
    address TEXT,
    marks DECIMAL(6,2) DEFAULT 0,
    attendance DECIMAL(6,2) DEFAULT 0,
    gpa DECIMAL(4,2) DEFAULT 0,
    study_hours DECIMAL(6,2) DEFAULT 0,
    backlogs INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- USERS TABLE (Admin / Faculty / Student login accounts)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'student') NOT NULL DEFAULT 'student',
    student_id INT DEFAULT NULL,
    faculty_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL,
    CONSTRAINT fk_users_faculty FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================================
-- PREDICTIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT DEFAULT NULL,
    score DECIMAL(8,2) NOT NULL,
    risk ENUM('Low', 'Medium', 'High') NOT NULL,
    probability DECIMAL(6,2) NOT NULL,
    predicted_by INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_predictions_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT fk_predictions_user FOREIGN KEY (predicted_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================================
-- COUNSELLING TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS counselling (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    faculty_id INT DEFAULT NULL,
    counselling_date DATE,
    status ENUM('Pending', 'Completed', 'Follow-up Required') DEFAULT 'Pending',
    notes TEXT,
    follow_up_date DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_counselling_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT fk_counselling_faculty FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_predictions_student ON predictions(student_id);
CREATE INDEX idx_predictions_risk ON predictions(risk);
CREATE INDEX idx_counselling_student ON counselling(student_id);
CREATE INDEX idx_students_department ON students(department);
CREATE INDEX idx_users_role ON users(role);