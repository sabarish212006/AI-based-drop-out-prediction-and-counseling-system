# AI-Based Student Dropout Prediction and Counselling System

## Project Overview

The AI-Based Student Dropout Prediction and Counselling System is a web-based application developed to identify students who are at risk of dropping out by analyzing their academic performance and related factors using Machine Learning. The system predicts the dropout risk level and provides appropriate counselling recommendations to help educational institutions take preventive actions at an early stage.

This project provides separate modules for Students, Counsellors, and Administrators, enabling efficient academic monitoring, risk prediction, counselling management, and report generation through a secure role-based platform.

---

## Objectives

- Predict student dropout risk using Machine Learning.
- Monitor students' academic performance continuously.
- Provide early counselling recommendations for at-risk students.
- Help institutions reduce student dropout rates.
- Generate academic reports and prediction summaries.
- Maintain secure access using role-based authentication.

---

## Key Features

### Student Module

- Student Registration and Login
- Profile Management
- Academic Record Management
- AI-Based Dropout Prediction
- Risk Score Visualization
- Academic Summary
- Prediction History
- Notifications

### Administrator Module

- Secure Admin Dashboard
- Student Management
- Counsellor Management
- Prediction Reports
- Excel Report Export
- PDF Report Generation
- Dashboard Statistics

### Counsellor Module

- High Risk Student Monitoring
- Student Profile Review
- Counselling Recommendations
- Counselling Notes Management
- Student Progress Tracking
- Risk Analytics Dashboard

### AI Prediction Module

- Machine Learning Based Prediction
- Risk Classification
- Risk Probability Calculation
- Recommendation Generation
- Prediction History Storage

---

## Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Chart.js |
| Authentication | Flask Session |
| PDF Generation | ReportLab |
| Excel Export | OpenPyXL |

---

## Machine Learning Model

The prediction model is trained using academic and behavioural attributes collected from students.

### Input Features

- CGPA
- Attendance Percentage
- Internal Marks
- Number of Backlogs
- Study Hours
- Semester
- Department
- Year of Study

### Prediction Output

- Low Risk
- Medium Risk
- High Risk

The generated prediction is further used to recommend suitable counselling actions for the student.

---

## System Modules

### Authentication Module

Provides secure login and role-based access for Students, Counsellors, and Administrators.

### Student Management Module

Allows students to maintain academic records and view AI prediction results.

### Academic Module

Stores semester-wise academic information including CGPA, attendance, internal marks, study hours, and backlog details.

### Prediction Module

Processes academic data through the Machine Learning model and generates risk predictions.

### Counselling Module

Allows counsellors to review predictions, schedule counselling sessions, and maintain counselling records.

### Report Module

Generates reports in PDF and Excel formats for academic monitoring and administrative purposes.

---

## Project Structure

```
AI-based-drop-out-prediction-and-counseling-system/

│
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   └── utils/
│
├── database/
│
├── trained_models/
│
├── requirements.txt
│
├── run.py
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/sabarish212006/AI-based-drop-out-prediction-and-counseling-system.git
```

### Navigate to Project Folder

```bash
cd AI-based-drop-out-prediction-and-counseling-system
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database

- Create a MySQL database.
- Import the SQL file available in the database folder.
- Update the database credentials in the configuration file.

### Run the Application

```bash
python run.py
```

The application will start on:

```
http://127.0.0.1:5000
```

---

## Future Enhancements

- Real-time student performance monitoring
- Email and SMS notification support
- Mobile application development
- Deep Learning based prediction model
- Parent Portal
- Faculty Performance Dashboard
- Cloud Deployment
- AI Chatbot for Student Guidance

---

## Conclusion

The AI-Based Student Dropout Prediction and Counselling System provides an intelligent solution for identifying students who are at risk of dropping out. By integrating Machine Learning with academic monitoring, the system enables educational institutions to perform early intervention through counselling and continuous performance tracking. This project demonstrates how Artificial Intelligence can support data-driven decision making and improve student success rates.

---

## Author

**Sabarish S**

Department of Artificial Intelligence and Machine Learning

VSB Engineering College

---

## License

This project was developed for academic and educational purposes as part of a Final Year Engineering Project.
