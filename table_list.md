# Table List

## Table 1: Student

| Field Name | Description |
|------------|-------------|
| Student_ID | Unique student identifier |
| Student_Name | Name of the student |
| Gender | Gender of the student |
| Department | Department name |
| Year_of_Study | Current year of study |
| Email | Student email address |
| Phone_Number | Student contact number |

## Table 2: Attendance

| Field Name | Description |
|------------|-------------|
| Attendance_ID | Unique attendance identifier |
| Student_ID | Student identifier |
| Attendance_Percentage | Attendance percentage |
| Total_Working_Days | Total working days |
| Days_Present | Number of days present |

## Table 3: Academic_Performance

| Field Name | Description |
|------------|-------------|
| Performance_ID | Unique performance identifier |
| Student_ID | Student identifier |
| Internal_Marks | Internal examination marks |
| Assignment_Score | Assignment score |
| CGPA | Current CGPA |
| Arrears | Number of arrears |

## Table 4: Dropout_Prediction

| Field Name | Description |
|------------|-------------|
| Prediction_ID | Unique prediction identifier |
| Student_ID | Student identifier |
| Risk_Level | Low, Medium or High risk |
| Prediction_Result | Dropout prediction result |
| Prediction_Date | Date of prediction |

## Table 5: Counseling

| Field Name | Description |
|------------|-------------|
| Counseling_ID | Unique counseling identifier |
| Student_ID | Student identifier |
| Recommendation | Counseling recommendation |
| Counseling_Date | Date of counseling |
| Counselor_Remarks | Counselor comments |

## Table 6: User_Login

| Field Name | Description |
|------------|-------------|
| User_ID | Unique user identifier |
| Username | Login username |
| Password | Login password |
| Role | Admin or Teacher |
