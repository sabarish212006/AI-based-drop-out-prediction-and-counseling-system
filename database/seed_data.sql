/*
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: seed_data.sql
Purpose: Insert Initial Sample Data
----------------------------------------------------------
Passwords (bcrypt hashed):
  Admin      : Admin@123
  Counsellors: Counsellor@123
  Students   : Student@123
----------------------------------------------------------
*/

USE dropout_prediction_db;

-- =====================================================
-- CLEAN EXISTING DATA (safe for development re-seed)
-- =====================================================
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM counselling_recommendations;
DELETE FROM dropout_predictions;
DELETE FROM behaviour_records;
DELETE FROM academic_records;
DELETE FROM students;
DELETE FROM login_history;
DELETE FROM notifications;
DELETE FROM system_logs;
DELETE FROM users;
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE students AUTO_INCREMENT = 1;
ALTER TABLE academic_records AUTO_INCREMENT = 1;
ALTER TABLE dropout_predictions AUTO_INCREMENT = 1;
ALTER TABLE counselling_recommendations AUTO_INCREMENT = 1;
ALTER TABLE notifications AUTO_INCREMENT = 1;
ALTER TABLE login_history AUTO_INCREMENT = 1;
ALTER TABLE system_logs AUTO_INCREMENT = 1;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- ADMIN USER (user_id = 1)
-- Password: Admin@123
-- =====================================================
INSERT INTO users (full_name, username, email, password_hash, role, phone)
VALUES (
    'System Administrator',
    'admin',
    'admin@college.edu',
    '$2b$12$EOWiuqiNc1b6AnsritUpvuT61Wa8lpHG83qX87YWpdNTPL/QJ/hde',
    'Admin',
    '9876543210'
);

-- =====================================================
-- COUNSELLORS (user_id = 2, 3)
-- Password: Counsellor@123
-- =====================================================
INSERT INTO users (full_name, username, email, password_hash, role, phone)
VALUES
(
    'Dr. Priya Sharma',
    'priya.counsellor',
    'priya.counsellor@college.edu',
    '$2b$12$q1Gw3d1Vso4leP2u4oLDjeLt7D/UsFe2ziTmhz4pEDW6meSV0Lc7G',
    'Counsellor',
    '9876543211'
),
(
    'Mr. Arun Kumar',
    'arun.counsellor',
    'arun.counsellor@college.edu',
    '$2b$12$q1Gw3d1Vso4leP2u4oLDjeLt7D/UsFe2ziTmhz4pEDW6meSV0Lc7G',
    'Counsellor',
    '9876543213'
);

-- =====================================================
-- STUDENTS (user_id = 4 to 23)
-- Email pattern: student01@college.edu ... student20@college.edu
-- Password: Student@123
-- =====================================================
INSERT INTO users (full_name, username, email, password_hash, role, phone)
VALUES
('Rahul Kumar',    'student01', 'student01@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000001'),
('Arun Prakash',   'student02', 'student02@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000002'),
('Priya Sharma',   'student03', 'student03@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000003'),
('Kavin Rajan',    'student04', 'student04@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000004'),
('Vignesh M',      'student05', 'student05@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000005'),
('Keerthana S',    'student06', 'student06@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000006'),
('Divya Lakshmi',  'student07', 'student07@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000007'),
('Nandhini P',     'student08', 'student08@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000008'),
('Harish V',       'student09', 'student09@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000009'),
('Ajay Krishna',   'student10', 'student10@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000010'),
('Sanjay R',       'student11', 'student11@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000011'),
('Rohit Verma',    'student12', 'student12@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000012'),
('Meena Devi',     'student13', 'student13@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000013'),
('Sneha Gupta',    'student14', 'student14@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000014'),
('Akash Singh',    'student15', 'student15@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000015'),
('Dinesh Babu',    'student16', 'student16@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000016'),
('Lokesh T',       'student17', 'student17@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000017'),
('Anitha R',       'student18', 'student18@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000018'),
('Varun Nair',     'student19', 'student19@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000019'),
('Sabarish M',     'student20', 'student20@college.edu', '$2b$12$WfRrB0IA.UPWVT5T8O2Hyuk6CjH6vJw/WlWMMbHhUv1yokihhVn26', 'Student', '9000000020');

-- =====================================================
-- STUDENTS TABLE — link users to students with roll numbers
-- =====================================================
INSERT INTO students (user_id, roll_no, department, year_of_study, gender, date_of_birth, address)
VALUES
(4,  '23CSE001', 'Computer Science and Engineering', 3, 'Male',   '2004-05-10', 'Chennai'),
(5,  '23CSE002', 'Computer Science and Engineering', 3, 'Male',   '2004-06-15', 'Coimbatore'),
(6,  '23CSE003', 'Computer Science and Engineering', 2, 'Female', '2005-03-22', 'Madurai'),
(7,  '23CSE004', 'Computer Science and Engineering', 4, 'Male',   '2003-11-01', 'Salem'),
(8,  '23CSE005', 'Electronics',                      3, 'Male',   '2004-07-08', 'Trichy'),
(9,  '23CSE006', 'Electronics',                      2, 'Female', '2005-01-30', 'Vellore'),
(10, '23CSE007', 'Information Technology',           3, 'Female', '2004-09-12', 'Chennai'),
(11, '23CSE008', 'Information Technology',           4, 'Female', '2003-04-25', 'Tirunelveli'),
(12, '23CSE009', 'Computer Science and Engineering', 2, 'Male',   '2005-08-14', 'Erode'),
(13, '23CSE010', 'Computer Science and Engineering', 3, 'Male',   '2004-02-19', 'Coimbatore'),
(14, '23CSE011', 'Electronics',                      4, 'Male',   '2003-06-07', 'Chennai'),
(15, '23CSE012', 'Information Technology',           2, 'Male',   '2005-10-03', 'Madurai'),
(16, '23CSE013', 'Computer Science and Engineering', 3, 'Female', '2004-12-20', 'Salem'),
(17, '23CSE014', 'Electronics',                      2, 'Female', '2005-05-17', 'Trichy'),
(18, '23CSE015', 'Information Technology',           4, 'Male',   '2003-09-28', 'Chennai'),
(19, '23CSE016', 'Computer Science and Engineering', 3, 'Male',   '2004-03-11', 'Vellore'),
(20, '23CSE017', 'Electronics',                      2, 'Female', '2005-07-04', 'Coimbatore'),
(21, '23CSE018', 'Information Technology',           3, 'Female', '2004-11-23', 'Madurai'),
(22, '23CSE019', 'Computer Science and Engineering', 4, 'Male',   '2003-08-16', 'Erode'),
(23, '23CSE020', 'Information Technology',           2, 'Male',   '2005-02-09', 'Salem');

-- =====================================================
-- ACADEMIC RECORDS — semester 5 (realistic varied data)
-- =====================================================
INSERT INTO academic_records (student_id, semester, cgpa, attendance, internal_marks, backlog_count, study_hours)
VALUES
(1,  5, 8.40, 86.50, 82.00, 0, 3.5),   -- Rahul: Good
(2,  5, 7.20, 73.50, 65.00, 0, 2.5),   -- Arun: Average-good, should be LOW risk
(3,  5, 9.10, 91.00, 88.00, 0, 5.0),   -- Priya: Excellent
(4,  5, 5.80, 62.00, 55.00, 3, 1.5),   -- Kavin: Poor, HIGH risk
(5,  5, 7.50, 78.50, 72.00, 1, 3.0),   -- Vignesh: Good
(6,  5, 6.20, 65.00, 58.00, 2, 2.0),   -- Keerthana: Average
(7,  5, 8.80, 89.00, 84.00, 0, 4.0),   -- Divya: Good
(8,  5, 4.90, 55.00, 42.00, 5, 1.0),   -- Nandhini: Very poor, HIGH risk
(9,  5, 7.80, 82.00, 76.00, 0, 3.5),   -- Harish: Good
(10, 5, 6.60, 70.00, 63.00, 1, 2.5),   -- Ajay: Average
(11, 5, 5.20, 58.00, 48.00, 4, 1.5),   -- Sanjay: Poor, MEDIUM-HIGH risk
(12, 5, 8.20, 85.00, 79.00, 0, 4.0),   -- Rohit: Good
(13, 5, 9.30, 93.00, 91.00, 0, 5.5),   -- Meena: Excellent
(14, 5, 6.90, 72.00, 67.00, 1, 2.5),   -- Sneha: Average
(15, 5, 7.60, 80.00, 74.00, 0, 3.0),   -- Akash: Good
(16, 5, 5.50, 60.00, 52.00, 3, 1.5),   -- Dinesh: Poor
(17, 5, 8.00, 84.00, 78.00, 0, 3.5),   -- Lokesh: Good
(18, 5, 4.60, 52.00, 40.00, 6, 1.0),   -- Anitha: Very poor, HIGH risk
(19, 5, 7.90, 83.00, 77.00, 0, 3.5),   -- Varun: Good
(20, 5, 6.80, 71.00, 64.00, 2, 2.0);   -- Sabarish: Average

-- Semester 4 records (history)
INSERT INTO academic_records (student_id, semester, cgpa, attendance, internal_marks, backlog_count, study_hours)
VALUES
(1,  4, 8.20, 84.00, 80.00, 0, 3.0),
(2,  4, 7.00, 70.00, 62.00, 0, 2.5),
(3,  4, 8.90, 90.00, 86.00, 0, 4.5),
(4,  4, 5.60, 60.00, 50.00, 4, 1.5),
(5,  4, 7.30, 76.00, 70.00, 1, 3.0),
(6,  4, 6.00, 63.00, 55.00, 2, 2.0),
(7,  4, 8.60, 87.00, 82.00, 0, 4.0),
(8,  4, 4.70, 52.00, 40.00, 5, 1.0),
(9,  4, 7.60, 80.00, 74.00, 0, 3.5),
(10, 4, 6.40, 68.00, 61.00, 1, 2.5);

-- =====================================================
-- BEHAVIOUR RECORDS
-- =====================================================
INSERT INTO behaviour_records (student_id, stress_level, discipline_score, participation_score, internet_access, family_income, parent_education, placement_interest, remarks)
VALUES
(1,  2, 85.00, 82.00, TRUE,  450000, 'Graduate',     TRUE,  'Consistent performance'),
(2,  3, 72.00, 68.00, TRUE,  320000, 'Graduate',     TRUE,  'Needs improvement in attendance'),
(3,  1, 92.00, 95.00, TRUE,  600000, 'Postgraduate', TRUE,  'Top performer'),
(4,  5, 55.00, 45.00, FALSE, 120000, 'School',       FALSE, 'At risk - needs immediate counselling'),
(5,  3, 78.00, 74.00, TRUE,  380000, 'Graduate',     TRUE,  'Good overall'),
(6,  4, 62.00, 58.00, TRUE,  250000, 'Diploma',      FALSE, 'Attendance concern'),
(7,  2, 88.00, 86.00, TRUE,  520000, 'Postgraduate', TRUE,  'Excellent participation'),
(8,  5, 45.00, 35.00, FALSE, 100000, 'School',       FALSE, 'High dropout risk'),
(9,  2, 80.00, 78.00, TRUE,  410000, 'Graduate',     TRUE,  'Performing well'),
(10, 3, 68.00, 64.00, TRUE,  290000, 'Diploma',      TRUE,  'Average performance'),
(11, 5, 52.00, 42.00, FALSE, 130000, 'School',       FALSE, 'Multiple backlogs'),
(12, 2, 82.00, 80.00, TRUE,  430000, 'Graduate',     TRUE,  'Good performance'),
(13, 1, 95.00, 93.00, TRUE,  650000, 'Postgraduate', TRUE,  'Exceptional student'),
(14, 3, 70.00, 66.00, TRUE,  300000, 'Graduate',     TRUE,  'Satisfactory'),
(15, 2, 79.00, 76.00, TRUE,  390000, 'Graduate',     TRUE,  'Good'),
(16, 4, 58.00, 50.00, FALSE, 140000, 'School',       FALSE, 'Low engagement'),
(17, 2, 81.00, 79.00, TRUE,  420000, 'Graduate',     TRUE,  'Consistent'),
(18, 5, 40.00, 32.00, FALSE, 90000,  'School',       FALSE, 'Severe risk - intervention needed'),
(19, 2, 82.00, 80.00, TRUE,  440000, 'Graduate',     TRUE,  'Doing well'),
(20, 3, 66.00, 62.00, TRUE,  280000, 'Diploma',      TRUE,  'Average');

-- =====================================================
-- DROPOUT PREDICTIONS — realistic risk distribution
-- =====================================================
INSERT INTO dropout_predictions (student_id, prediction_result, probability, risk_level, explanation, model_version)
VALUES
(1,  'No dropout risk',       12.50, 'Low',    'CGPA 8.4, attendance 86.5%, no backlogs. Student performing well.', 'v1'),
(2,  'No dropout risk',       28.00, 'Low',    'CGPA 7.2, attendance 73.5%, no backlogs. Acceptable performance.', 'v1'),
(3,  'No dropout risk',        5.20, 'Low',    'CGPA 9.1, attendance 91%, excellent performance.', 'v1'),
(4,  'High dropout risk',     82.50, 'High',   'CGPA 5.8, attendance 62%, 3 backlogs. Immediate intervention needed.', 'v1'),
(5,  'No dropout risk',       22.00, 'Low',    'CGPA 7.5, attendance 78.5%, 1 backlog. Generally good.', 'v1'),
(6,  'Medium dropout risk',   48.00, 'Medium', 'CGPA 6.2, attendance 65%, 2 backlogs. Monitoring recommended.', 'v1'),
(7,  'No dropout risk',        8.00, 'Low',    'CGPA 8.8, attendance 89%, no backlogs. Good student.', 'v1'),
(8,  'High dropout risk',     91.00, 'High',   'CGPA 4.9, attendance 55%, 5 backlogs. Critical intervention required.', 'v1'),
(9,  'No dropout risk',       18.00, 'Low',    'CGPA 7.8, attendance 82%, no backlogs. Performing well.', 'v1'),
(10, 'No dropout risk',       35.00, 'Medium', 'CGPA 6.6, attendance 70%, 1 backlog. Needs improvement.', 'v1'),
(11, 'High dropout risk',     75.00, 'High',   'CGPA 5.2, attendance 58%, 4 backlogs. High risk.', 'v1'),
(12, 'No dropout risk',       15.00, 'Low',    'CGPA 8.2, attendance 85%, no backlogs. Good performance.', 'v1'),
(13, 'No dropout risk',        3.50, 'Low',    'CGPA 9.3, attendance 93%, no backlogs. Excellent student.', 'v1'),
(14, 'No dropout risk',       30.00, 'Low',    'CGPA 6.9, attendance 72%, 1 backlog. Satisfactory.', 'v1'),
(15, 'No dropout risk',       20.00, 'Low',    'CGPA 7.6, attendance 80%, no backlogs. Good.', 'v1'),
(16, 'Medium dropout risk',   58.00, 'Medium', 'CGPA 5.5, attendance 60%, 3 backlogs. Needs counselling.', 'v1'),
(17, 'No dropout risk',       16.00, 'Low',    'CGPA 8.0, attendance 84%, no backlogs. Consistent.', 'v1'),
(18, 'High dropout risk',     88.00, 'High',   'CGPA 4.6, attendance 52%, 6 backlogs. Severe risk.', 'v1'),
(19, 'No dropout risk',       14.00, 'Low',    'CGPA 7.9, attendance 83%, no backlogs. Doing well.', 'v1'),
(20, 'No dropout risk',       32.00, 'Medium', 'CGPA 6.8, attendance 71%, 2 backlogs. Average.', 'v1');

-- =====================================================
-- COUNSELLING RECOMMENDATIONS
-- High/Medium risk students get counselling notes
-- =====================================================
INSERT INTO counselling_recommendations (prediction_id, counsellor_id, recommendation, follow_up_date, status)
VALUES
(4,  2, 'Immediate academic intervention required. Schedule weekly mentoring sessions. Target attendance above 75% and clear pending backlogs.', DATE_ADD(CURDATE(), INTERVAL 7 DAY),  'Pending'),
(6,  3, 'Monitor attendance closely. Assign a student mentor. Recommend study group participation.', DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'Pending'),
(8,  2, 'Critical case. Family counselling may be required. Arrange remedial classes for all failed subjects.', DATE_ADD(CURDATE(), INTERVAL 3 DAY),  'Pending'),
(10, 3, 'Attendance improvement plan needed. Advise student on time management and study skills.', DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'Completed'),
(11, 2, 'Multiple backlogs detected. Academic support plan initiated. Follow up fortnightly.', DATE_ADD(CURDATE(), INTERVAL 5 DAY),  'Pending'),
(16, 3, 'Needs motivational counselling. Low participation and engagement noted.', DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'Pending'),
(18, 2, 'Most severe case. Family background check recommended. Emergency intervention session scheduled.', DATE_ADD(CURDATE(), INTERVAL 2 DAY),  'Pending'),
(20, 3, 'Average performance with scope for improvement. Bi-weekly progress review recommended.', DATE_ADD(CURDATE(), INTERVAL 21 DAY), 'Completed');

-- =====================================================
-- NOTIFICATIONS
-- =====================================================
INSERT INTO notifications (user_id, title, message)
SELECT
    s.user_id,
    'AI Prediction Ready',
    CONCAT('Your dropout risk prediction is available. Risk Level: ', p.risk_level, '. Please check your dashboard.')
FROM students s
JOIN dropout_predictions p ON p.student_id = s.student_id;

-- Counsellor notifications
INSERT INTO notifications (user_id, title, message)
VALUES
(2, 'New Student Assignment', '4 high/medium risk students assigned for counselling.'),
(3, 'New Student Assignment', '4 high/medium risk students assigned for counselling.'),
(1, 'System Ready', 'AI Dropout Prediction System is fully operational with 20 students.');

-- =====================================================
-- LOGIN HISTORY (sample)
-- =====================================================
INSERT INTO login_history (user_id, ip_address, status)
VALUES
(1, '127.0.0.1', 'Success'),
(2, '127.0.0.1', 'Success'),
(3, '127.0.0.1', 'Success'),
(4, '127.0.0.1', 'Success'),
(5, '127.0.0.1', 'Success');

-- =====================================================
-- SYSTEM LOGS
-- =====================================================
INSERT INTO system_logs (log_level, module_name, log_message)
VALUES
('INFO', 'Database', 'Initial seed data inserted successfully.'),
('INFO', 'ML Model', 'Dropout prediction model v1 loaded.'),
('INFO', 'System',   'Application startup complete.');