CREATE DATABASE IF NOT EXISTS dropout_prediction_db;
USE dropout_prediction_db;

-- =====================================================
-- USERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    username      VARCHAR(50)  UNIQUE,
    email         VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('Admin','Student','Counsellor') NOT NULL,
    phone         VARCHAR(15),
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- STUDENTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS students (
    student_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT UNIQUE NOT NULL,
    roll_no      VARCHAR(20) UNIQUE NOT NULL,
    department   VARCHAR(100),
    year_of_study INT,
    gender       ENUM('Male','Female','Other'),
    date_of_birth DATE,
    address      TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- ACADEMIC RECORDS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS academic_records (
    academic_id    INT AUTO_INCREMENT PRIMARY KEY,
    student_id     INT NOT NULL,
    semester       INT,
    cgpa           DECIMAL(4,2),
    attendance     DECIMAL(5,2),
    internal_marks DECIMAL(5,2),
    backlog_count  INT DEFAULT 0,
    study_hours    DECIMAL(4,2),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- =====================================================
-- BEHAVIOUR RECORDS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS behaviour_records (
    behaviour_id        INT AUTO_INCREMENT PRIMARY KEY,
    student_id          INT NOT NULL,
    stress_level        INT,
    discipline_score    DECIMAL(5,2),
    participation_score DECIMAL(5,2),
    internet_access     BOOLEAN,
    family_income       DECIMAL(12,2),
    parent_education    VARCHAR(100),
    placement_interest  BOOLEAN,
    remarks             TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- =====================================================
-- DROPOUT PREDICTIONS TABLE
-- Column: probability (consistent across all code)
-- =====================================================
CREATE TABLE IF NOT EXISTS dropout_predictions (
    prediction_id    INT AUTO_INCREMENT PRIMARY KEY,
    student_id       INT NOT NULL,
    prediction_result TEXT,
    probability      DECIMAL(6,2),
    risk_level       ENUM('Low','Medium','High'),
    explanation      TEXT,
    model_version    VARCHAR(20),
    predicted_on     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- =====================================================
-- COUNSELLING RECOMMENDATIONS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS counselling_recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id     INT,
    counsellor_id     INT,
    recommendation    TEXT,
    follow_up_date    DATE,
    status            ENUM('Pending','In Progress','Completed') DEFAULT 'Pending',
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id)  REFERENCES dropout_predictions(prediction_id) ON DELETE SET NULL,
    FOREIGN KEY (counsellor_id)  REFERENCES users(user_id) ON DELETE SET NULL
);

-- =====================================================
-- NOTIFICATIONS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT,
    title           VARCHAR(150),
    message         TEXT,
    is_read         BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =====================================================
-- LOGIN HISTORY TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS login_history (
    login_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    status     ENUM('Success','Failed'),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =====================================================
-- SYSTEM LOGS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS system_logs (
    log_id      INT AUTO_INCREMENT PRIMARY KEY,
    log_level   VARCHAR(20),
    module_name VARCHAR(100),
    log_message TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES (Performance)
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_students_roll     ON students(roll_no);
CREATE INDEX IF NOT EXISTS idx_predictions_student ON dropout_predictions(student_id);
CREATE INDEX IF NOT EXISTS idx_predictions_risk    ON dropout_predictions(risk_level);
CREATE INDEX IF NOT EXISTS idx_academic_student   ON academic_records(student_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, is_read);
