CREATE TABLE Student (
    Student_ID INT PRIMARY KEY,
    Student_Name VARCHAR(100),
    Gender VARCHAR(10),
    Department VARCHAR(50),
    Year_of_Study INT,
    Email VARCHAR(100),
    Phone_Number VARCHAR(15)
);

CREATE TABLE Attendance (
    Attendance_ID INT PRIMARY KEY,
    Student_ID INT,
    Attendance_Percentage FLOAT,
    Total_Working_Days INT,
    Days_Present INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
);

CREATE TABLE Academic_Performance (
    Performance_ID INT PRIMARY KEY,
    Student_ID INT,
    Internal_Marks FLOAT,
    Assignment_Score FLOAT,
    CGPA FLOAT,
    Arrears INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
);

CREATE TABLE Dropout_Prediction (
    Prediction_ID INT PRIMARY KEY,
    Student_ID INT,
    Risk_Level VARCHAR(20),
    Prediction_Result VARCHAR(50),
    Prediction_Date DATE,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
);

CREATE TABLE Counseling (
    Counseling_ID INT PRIMARY KEY,
    Student_ID INT,
    Recommendation TEXT,
    Counseling_Date DATE,
    Counselor_Remarks TEXT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID)
);

CREATE TABLE User_Login (
    User_ID INT PRIMARY KEY,
    Username VARCHAR(50),
    Password VARCHAR(100),
    Role VARCHAR(20)
);
