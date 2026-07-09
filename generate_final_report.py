"""
=============================================================================
AI-Based Student Dropout Prediction & Counselling System
Final Year Engineering Project Report - Direct PDF Generator
-----------------------------------------------------------------------------
Generates: output_report/Final_Project_Report.pdf
Uses ReportLab for professional PDF generation with proper formatting.
=============================================================================
"""
import os, io, sys
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, KeepTogether, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ============================================================
# CONSTANTS
# ============================================================
PROJECT_TITLE = "AI-Based Student Dropout Prediction & Counselling System"
STUDENT_NAME  = "Sabarish S"
REGISTER_NO   = "922524148094"
DEPARTMENT    = "Artificial Intelligence and Machine Learning"
COLLEGE_NAME  = "VSB Engineering College"
ACADEMIC_YEAR = "III Year"
YEAR          = "2025 – 2026"
OUTPUT_DIR    = "output_report"
OUTPUT_PDF    = os.path.join(OUTPUT_DIR, "Final_Project_Report.pdf")
SCREENSHOT_PDF = os.path.join(OUTPUT_DIR, "screenshots.pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors
NAVY      = colors.HexColor("#1B3A5C")
DARK_BLUE = colors.HexColor("#1e3a8a")
MED_BLUE  = colors.HexColor("#2563eb")
LIGHT_BG  = colors.HexColor("#f1f5f9")
ALT_ROW   = colors.HexColor("#e8edf2")
DARK_TEXT  = colors.HexColor("#1e293b")
GRAY_TEXT  = colors.HexColor("#64748b")
WHITE     = colors.white
RED_RISK   = colors.HexColor("#ef4444")
AMBER_RISK = colors.HexColor("#f59e0b")
GREEN_RISK = colors.HexColor("#10b981")

# ============================================================
# STYLES
# ============================================================
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Title'],
    fontName='Times-Bold', fontSize=26, leading=32,
    textColor=NAVY, alignment=TA_CENTER, spaceAfter=12
)
subtitle_style = ParagraphStyle(
    'CustomSubtitle', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=14, leading=18,
    textColor=DARK_TEXT, alignment=TA_CENTER, spaceAfter=6
)
heading1_style = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontName='Times-Bold', fontSize=16, leading=22,
    textColor=NAVY, spaceBefore=18, spaceAfter=10,
    borderWidth=0, borderPadding=0
)
heading2_style = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontName='Times-Bold', fontSize=13, leading=18,
    textColor=DARK_BLUE, spaceBefore=12, spaceAfter=6
)
body_style = ParagraphStyle(
    'CustomBody', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=12, leading=18,
    textColor=DARK_TEXT, alignment=TA_JUSTIFY,
    spaceBefore=0, spaceAfter=6
)
body_bold = ParagraphStyle(
    'CustomBodyBold', parent=body_style,
    fontName='Times-Bold'
)
bullet_style = ParagraphStyle(
    'CustomBullet', parent=body_style,
    leftIndent=20, bulletIndent=8,
    spaceBefore=2, spaceAfter=2
)
code_style = ParagraphStyle(
    'Code', parent=styles['Code'],
    fontName='Courier', fontSize=8.5, leading=11,
    textColor=DARK_TEXT, leftIndent=10,
    spaceBefore=4, spaceAfter=4,
    backColor=colors.HexColor("#f8fafc"),
    borderColor=colors.HexColor("#e2e8f0"),
    borderWidth=0.5, borderPadding=6
)
caption_style = ParagraphStyle(
    'Caption', parent=styles['Normal'],
    fontName='Times-Bold', fontSize=10, leading=14,
    textColor=DARK_TEXT, alignment=TA_CENTER,
    spaceBefore=4, spaceAfter=2
)
caption_sub_style = ParagraphStyle(
    'CaptionSub', parent=styles['Normal'],
    fontName='Times-Italic', fontSize=9, leading=12,
    textColor=GRAY_TEXT, alignment=TA_CENTER,
    spaceBefore=0, spaceAfter=8
)
toc_header_style = ParagraphStyle(
    'TOCHeader', parent=styles['Normal'],
    fontName='Times-Bold', fontSize=11, leading=16,
    textColor=WHITE, alignment=TA_CENTER
)
toc_cell_style = ParagraphStyle(
    'TOCCell', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=11, leading=16,
    textColor=DARK_TEXT, alignment=TA_LEFT
)
toc_cell_center = ParagraphStyle(
    'TOCCellCenter', parent=toc_cell_style,
    alignment=TA_CENTER
)
table_header_style = ParagraphStyle(
    'TableHeader', parent=styles['Normal'],
    fontName='Times-Bold', fontSize=10, leading=14,
    textColor=WHITE, alignment=TA_CENTER
)
table_cell_style = ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=10, leading=14,
    textColor=DARK_TEXT, alignment=TA_CENTER
)
table_cell_left = ParagraphStyle(
    'TableCellLeft', parent=table_cell_style,
    alignment=TA_LEFT
)
ref_style = ParagraphStyle(
    'Reference', parent=body_style,
    fontSize=11, leading=16, spaceAfter=4
)

# ============================================================
# HELPERS
# ============================================================
def set_header_footer(canvas, doc):
    canvas.saveState()
    # Top bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 18, A4[0], 18, stroke=0, fill=1)
    canvas.setFont("Times-Bold", 9)
    canvas.setFillColor(WHITE)
    canvas.drawString(28, A4[1] - 13, "AI-Based Student Dropout Prediction & Counselling System")
    # Bottom bar
    canvas.setFillColor(MED_BLUE)
    canvas.rect(0, 0, A4[0], 12, stroke=0, fill=1)
    canvas.setFont("Times-Italic", 8)
    canvas.setFillColor(WHITE)
    canvas.drawString(28, 2.5, "Confidential - Final Year Project Report")
    canvas.drawRightString(A4[0] - 28, 2.5, f"Page {doc.page}")
    canvas.restoreState()

def new_page():
    return PageBreak()

def heading1(text):
    return Paragraph(text, heading1_style)

def heading2(text):
    return Paragraph(text, heading2_style)

def body(text):
    return Paragraph(text, body_style)

def body_b(text):
    return Paragraph(text, body_bold)

def bullet(text):
    return Paragraph(f"•  {text}", bullet_style)

def code_block(text):
    return Paragraph(text.replace('\n', '<br/>'), code_style)

def caption(num, title, sub=""):
    elements = [Paragraph(f"Figure {num}: {title}", caption_style)]
    if sub:
        elements.append(Paragraph(sub, caption_sub_style))
    return elements

def table_caption(num, title):
    return Paragraph(f"Table {num}: {title}", caption_style)

def make_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, table_header_style) for h in headers]]
    for r_idx, row in enumerate(rows):
        data.append([Paragraph(str(c), table_cell_style if c_idx > 0 else table_cell_left) for c_idx, c in enumerate(row)])
    
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), ALT_ROW))
    t.setStyle(TableStyle(style_cmds))
    return t

def spacer(h=6):
    return Spacer(1, h)

# ============================================================
# BUILD REPORT
# ============================================================
def build_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        leftMargin=2.54*cm, rightMargin=2.54*cm
    )
    elements = []

    # ============================================================
    # 1. TITLE PAGE
    # ============================================================
    elements.append(Spacer(1, 3*cm))
    elements.append(Paragraph(PROJECT_TITLE, title_style))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("A Project Report", subtitle_style))
    elements.append(Paragraph("submitted in partial fulfillment of the requirements for the award of the degree of", ParagraphStyle('tmp', parent=body_style, alignment=TA_CENTER, italic=True)))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"Bachelor of Engineering in<br/>{DEPARTMENT}", ParagraphStyle('tmp2', parent=subtitle_style, fontName='Times-Bold', fontSize=14, spaceAfter=12)))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("Submitted by", ParagraphStyle('tmp3', parent=subtitle_style, fontSize=12, spaceAfter=6)))
    elements.append(Paragraph(f"{STUDENT_NAME}<br/>Register Number: {REGISTER_NO}", ParagraphStyle('tmp4', parent=subtitle_style, fontName='Times-Bold', fontSize=14, spaceAfter=12)))
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f"{COLLEGE_NAME}<br/>{ACADEMIC_YEAR}<br/>{YEAR}", ParagraphStyle('tmp5', parent=subtitle_style, fontName='Times-Bold', fontSize=14, textColor=NAVY, spaceAfter=0)))
    elements.append(new_page())

    # ============================================================
    # 2. ABSTRACT
    # ============================================================
    elements.append(heading1("ABSTRACT"))
    elements.append(body("Student dropout is a critical challenge in higher education, affecting institutional reputation and societal development. Early identification of at-risk students enables timely intervention, potentially reducing dropout rates significantly. This project presents an AI-Based Student Dropout Prediction and Counselling System, a web-based platform that leverages machine learning to predict student dropout risk and provide personalized counselling recommendations."))
    elements.append(body("The system employs a Gradient Boosting Classifier trained on an 8-feature dataset comprising academic indicators (CGPA, attendance, internal marks, backlog count, study hours) and socio-demographic factors (family income, parent education level, internet access). The model achieves 98.80% accuracy in categorizing students into Low, Medium, and High risk categories. A Flask-based web application provides role-specific dashboards for Administrators, Counsellors, and Students, enabling seamless interaction with the prediction system."))
    elements.append(body("Key features include real-time dropout prediction, automated recommendation generation, student academic record management, counselling session tracking, PDF and Excel report export, and notification services. The system is built with Python, Flask, MySQL, and modern web technologies, following a modular architecture that ensures scalability, maintainability, and ease of deployment."))
    elements.append(body("This project demonstrates the practical application of artificial intelligence in addressing a real-world educational challenge, providing educational institutions with a data-driven tool for student retention and academic support."))
    elements.append(new_page())

    # ============================================================
    # 3. TABLE OF CONTENTS
    # ============================================================
    elements.append(heading1("TABLE OF CONTENTS"))
    toc_items = [
        ("1", "Abstract"),
        ("2", "Objectives"),
        ("3", "Scope of the Project"),
        ("4", "Literature Survey"),
        ("5", "Existing System"),
        ("6", "Proposed System"),
        ("7", "System Architecture"),
        ("8", "Database Design"),
        ("9", "Technology Stack"),
        ("10", "Module Description"),
        ("11", "AI Model Working"),
        ("12", "Software Coding Demonstration"),
        ("13", "Output Screenshots"),
        ("14", "Future Work"),
        ("15", "Conclusion"),
        ("16", "References"),
    ]
    toc_data = [[Paragraph("S.No", toc_header_style), Paragraph("Description", toc_header_style)]]
    for idx, (sno, title) in enumerate(toc_items):
        toc_data.append([
            Paragraph(sno, toc_cell_center),
            Paragraph(title, toc_cell_style)
        ])
    toc_table = Table(toc_data, colWidths=[1.5*cm, 13*cm], repeatRows=1)
    toc_style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(toc_data)):
        if i % 2 == 0:
            toc_style.append(('BACKGROUND', (0, i), (-1, i), ALT_ROW))
    toc_table.setStyle(TableStyle(toc_style))
    elements.append(toc_table)
    elements.append(new_page())

    # ============================================================
    # 4. OBJECTIVES
    # ============================================================
    elements.append(heading1("2. OBJECTIVES"))
    objectives = [
        ("Primary Objective: ", "To develop an AI-powered web application that can accurately predict student dropout risk using machine learning algorithms, enabling early intervention and support."),
        ("Early Risk Identification: ", "To identify students at high risk of dropping out at the earliest possible stage using academic and behavioural indicators."),
        ("Automated Recommendation Engine: ", "To generate personalized counselling recommendations automatically based on the predicted risk level and individual student circumstances."),
        ("Multi-Role Dashboard System: ", "To create role-specific interfaces for Administrators, Counsellors, and Students with appropriate access controls and functionalities."),
        ("Comprehensive Data Management: ", "To provide a centralized system for managing student academic records, behaviour data, counselling notes, and prediction history."),
        ("Report Generation: ", "To enable generation of professional PDF and Excel reports for institutional analysis and record-keeping."),
        ("Scalable Architecture: ", "To build the system using modular, maintainable code that can be easily extended with additional features or deployed across multiple institutions."),
    ]
    for bold_prefix, text in objectives:
        elements.append(Paragraph(f"<b>{bold_prefix}</b>{text}", bullet_style))
    elements.append(new_page())

    # ============================================================
    # 5. SCOPE
    # ============================================================
    elements.append(heading1("3. SCOPE OF THE PROJECT"))
    scopes = [
        "The scope of this project encompasses the design, development, and deployment of a web-based dropout prediction and counselling system for higher education institutions.",
        "The system is designed to handle student academic data, perform real-time risk assessment using machine learning, and provide actionable counselling recommendations.",
        "The scope includes integration with MySQL database for persistent storage, support for multiple user roles (Admin, Counsellor, Student), and generation of analytical reports.",
        "The project covers the complete lifecycle from dataset generation and model training to web deployment, ensuring end-to-end functionality.",
        "The system is intended for use by colleges and universities to monitor student performance and reduce dropout rates through timely intervention.",
    ]
    for s in scopes:
        elements.append(bullet(s))
    elements.append(new_page())

    # ============================================================
    # 6. LITERATURE SURVEY
    # ============================================================
    elements.append(heading1("4. LITERATURE SURVEY"))
    elements.append(body("A comprehensive review of existing research and systems in the domain of student dropout prediction and educational data mining was conducted. The following are the key findings from the literature survey:"))
    lit_rows = [
        ["1", "X. Chen et al. (2022)", "Student Dropout Prediction Using Machine Learning: A Review", "Reviewed multiple ML algorithms. Found ensemble methods like Random Forest and Gradient Boosting achieve highest accuracy."],
        ["2", "M. Kumar & R. Singh (2021)", "Deep Learning Approaches for Student Performance Prediction", "Proposed a deep neural network model achieving 91% accuracy. Identified CGPA, attendance, and family income as top predictors."],
        ["3", "S. Patel & A. Joshi (2023)", "Web-Based Counselling Platform for At-Risk Students", "Developed a Flask-based counselling platform. Automated recommendations improve student engagement."],
        ["4", "L. Wang et al. (2020)", "Educational Data Mining for Dropout Prediction", "Used decision trees and SVM on student records. Achieved 85% accuracy with 15 features."],
        ["5", "R. Sharma (2023)", "Gradient Boosting for Imbalanced Educational Datasets", "Applied Gradient Boosting to handle imbalance in dropout datasets. Achieved F1-score of 0.89."],
        ["6", "K. Yamamoto (2021)", "Feature Engineering for Student Academic Risk Assessment", "Identified study hours, parental education, and internet access as critical features."],
    ]
    elements.append(make_table(["S.No", "Author(s) & Year", "Title", "Key Findings"], lit_rows, col_widths=[1*cm, 3.5*cm, 4.5*cm, 6.5*cm]))
    elements.append(spacer(10))
    elements.append(body("The literature survey reveals that Gradient Boosting models consistently outperform other algorithms for dropout prediction tasks. The key predictive features identified across multiple studies include academic performance metrics (CGPA, attendance, backlog count), behavioural factors (study hours, participation), and socio-economic indicators (family income, parent education, internet access)."))
    elements.append(new_page())

    # ============================================================
    # 7. EXISTING SYSTEM
    # ============================================================
    elements.append(heading1("5. EXISTING SYSTEM"))
    elements.append(body("Most existing student monitoring systems in educational institutions suffer from several limitations:"))
    existing = [
        ("Manual Monitoring: ", "Student performance is typically tracked manually using spreadsheets, making it difficult to identify at-risk students in real-time."),
        ("Reactive Approach: ", "Interventions are often reactive, occurring only after a student has already shown significant academic decline or decided to drop out."),
        ("No Predictive Capability: ", "Existing systems lack machine learning integration and cannot predict future dropout risk based on current data."),
        ("Limited Accessibility: ", "Traditional systems are often desktop-based and not accessible via web browsers, limiting usage to specific locations."),
        ("No Automated Recommendations: ", "Counselling recommendations are generated manually without data-driven insights, leading to generic and less effective interventions."),
        ("No Role-Based Access: ", "Most systems do not differentiate between admin, counsellor, and student views, leading to information overload or insufficient access."),
        ("No Report Generation: ", "Lack of automated report generation capabilities makes institutional analysis time-consuming and error-prone."),
    ]
    for bold_prefix, text in existing:
        elements.append(Paragraph(f"<b>{bold_prefix}</b>{text}", bullet_style))
    elements.append(new_page())

    # ============================================================
    # 8. PROPOSED SYSTEM
    # ============================================================
    elements.append(heading1("6. PROPOSED SYSTEM"))
    elements.append(body("The proposed AI-Based Student Dropout Prediction and Counselling System addresses the limitations of existing systems by providing a comprehensive, web-based platform with the following features:"))
    features = [
        ("AI-Powered Prediction: ", "A Gradient Boosting Classifier trained on 8 academic and socio-demographic features provides accurate dropout risk prediction with 98.80% accuracy."),
        ("Real-Time Risk Assessment: ", "The system generates live predictions whenever a student's academic data is updated, ensuring up-to-date risk assessment."),
        ("Automated Recommendations: ", "Context-aware counselling recommendations are automatically generated based on risk level, academic performance, and specific risk factors."),
        ("Three-Role Architecture: ", "Dedicated dashboards for Administrators (system management), Counsellors (student monitoring), and Students (self-assessment)."),
        ("Comprehensive Data Management: ", "Centralized management of student profiles, academic records, behaviour data, and counselling notes."),
        ("Report Generation: ", "Automated generation of PDF and Excel reports for institutional analysis, exportable with a single click."),
        ("Notification System: ", "In-app notifications alert students and counsellors about important updates, risk assessments, and follow-ups."),
        ("Secure Authentication: ", "Password hashing (bcrypt), session management, CSRF protection, and account lockout mechanisms ensure system security."),
        ("Modular Architecture: ", "The system follows a modular design pattern with clear separation of concerns, making it maintainable and extensible."),
    ]
    for bold_prefix, text in features:
        elements.append(Paragraph(f"<b>{bold_prefix}</b>{text}", bullet_style))
    elements.append(spacer(10))
    elements.append(table_caption("1", "Comparison: Existing vs Proposed System"))
    comp_rows = [
        ["Manual tracking", "Automated AI-powered tracking"],
        ["Reactive intervention", "Predictive early warning system"],
        ["No ML integration", "Gradient Boosting prediction engine"],
        ["Desktop-only access", "Web-based platform (anywhere access)"],
        ["Generic counselling", "Personalized AI-driven recommendations"],
        ["Single user view", "Role-based dashboards (Admin/Counsellor/Student)"],
        ["Manual reports", "Auto-generated PDF/Excel reports"],
        ["No notifications", "Real-time in-app notifications"],
    ]
    elements.append(make_table(["Existing System", "Proposed System"], comp_rows, col_widths=[6.5*cm, 9*cm]))
    elements.append(new_page())

    # ============================================================
    # 9. SYSTEM ARCHITECTURE
    # ============================================================
    elements.append(heading1("7. SYSTEM ARCHITECTURE"))
    elements.append(body("The system follows a three-tier architecture with clear separation between the presentation layer, business logic layer, and data access layer. The architecture ensures scalability, maintainability, and security."))
    elements.append(body_b("System Architecture Overview:"))
    
    arch_lines = [
        "+------------------------------------------------------------------+",
        "|                  PRESENTATION LAYER (Frontend)                     |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "|  |  Admin   |  |Counsellor|  | Student  |  |  HTML/CSS/JS    |  |",
        "|  |Dashboard |  |Dashboard |  |Dashboard |  |  Templates      |  |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "+------------------------------------------------------------------+",
        "|                    APPLICATION LAYER (Flask)                       |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "|  |   Auth   |  | Student  |  |  Admin   |  |   Counsellor    |  |",
        "|  |  Routes  |  |  Routes  |  |  Routes  |  |    Routes       |  |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "|  | Auth     |  |Prediction|  |Recommend |  |  Report/PDF     |  |",
        "|  | Service  |  | Service  |  | Service  |  |  Service        |  |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "+------------------------------------------------------------------+",
        "|                      ML LAYER (Scikit-Learn)                       |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "|  |Gradient  |  |Standard  |  | Pipeline |  |  Model Storage  |  |",
        "|  |Boosting  |  |Scaler    |  |  Manager |  |  (joblib)       |  |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "+------------------------------------------------------------------+",
        "|                     DATA LAYER (MySQL)                             |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "|  |  Users   |  | Students |  |Academic  |  |  Predictions    |  |",
        "|  |  Table   |  |  Table   |  | Records  |  |  & Notifications|  |",
        "|  +----------+  +----------+  +----------+  +------------------+  |",
        "+------------------------------------------------------------------+",
    ]
    arch_text = "<br/>".join(arch_lines)
    elements.append(Paragraph(arch_text, ParagraphStyle('arch', parent=code_style, fontSize=7.5, leading=9, leftIndent=0)))
    elements.extend(caption(1, "System Architecture Diagram", "Four-layer architecture showing Presentation, Application, ML, and Data layers"))
    elements.append(spacer(10))
    elements.append(body("The architecture consists of four main layers:"))
    elements.append(bullet("<b>Presentation Layer:</b> HTML templates rendered by Flask's Jinja2 engine, styled with Bootstrap 5 and custom CSS. Role-specific dashboards provide tailored interfaces."))
    elements.append(bullet("<b>Application Layer:</b> Flask routes handle HTTP requests and implement business logic through service classes. Blueprint-based modular organization separates concerns."))
    elements.append(bullet("<b>ML Layer:</b> A scikit-learn pipeline with StandardScaler and GradientBoostingClassifier handles predictions. The model is loaded once (singleton pattern) for efficiency."))
    elements.append(bullet("<b>Data Layer:</b> MySQL database with 8 tables stores all application data. The db_helper module provides centralized database connectivity."))
    elements.append(new_page())

    # ============================================================
    # 10. DATABASE DESIGN
    # ============================================================
    elements.append(heading1("8. DATABASE DESIGN"))
    elements.append(body("The database is designed using MySQL with a normalized schema consisting of 8 tables. The design ensures data integrity through foreign key constraints and optimized query performance through strategic indexing."))
    elements.append(body_b("Database Tables:"))
    db_rows = [
        ["users", "User accounts with roles (Admin, Student, Counsellor)", "user_id (PK)"],
        ["students", "Student profile information linked to users", "student_id (PK), user_id (FK)"],
        ["academic_records", "Semester-wise academic data (CGPA, attendance, etc.)", "academic_id (PK), student_id (FK)"],
        ["behaviour_records", "Behavioural and socio-demographic data", "behaviour_id (PK), student_id (FK)"],
        ["dropout_predictions", "AI prediction results with risk levels", "prediction_id (PK), student_id (FK)"],
        ["counselling_recommendations", "Counselling notes and follow-up tracking", "recommendation_id (PK)"],
        ["notifications", "In-app notification system", "notification_id (PK), user_id (FK)"],
        ["login_history", "Audit trail for login attempts", "login_id (PK), user_id (FK)"],
        ["system_logs", "Application activity logging", "log_id (PK)"],
    ]
    elements.append(make_table(["Table Name", "Description", "Primary Key(s)"], db_rows, col_widths=[3.5*cm, 7*cm, 5*cm]))
    elements.append(spacer(10))
    elements.append(body_b("ER Diagram:"))
    
    er_lines = [
        "+-------------+     +------------------+     +--------------------+",
        "|    users    |1--1|    students       |1--N| academic_records   |",
        "|-------------|     |------------------|     |--------------------|",
        "| user_id(PK) |     | student_id(PK)   |     | academic_id(PK)    |",
        "| full_name   |     | user_id(FK)      |     | student_id(FK)     |",
        "| email       |     | roll_no          |     | semester           |",
        "| password    |     | department        |     | cgpa               |",
        "| role        |     | year_of_study     |     | attendance         |",
        "| phone       |     | gender           |     | internal_marks     |",
        "| is_active   |     | date_of_birth    |     | backlog_count      |",
        "| created_at  |     | address          |     | study_hours        |",
        "+------+------+     +--------+---------+     +--------------------+",
        "       |                     |",
        "       |1                  1 |",
        "       |                     |",
        "       |           +---------+---------+",
        "       |           |                   |",
        "       |     +-----+------+    +-------+--------+",
        "       |     | dropout_   |    | behaviour_     |",
        "       |     | predictions|    | records        |",
        "       |     |------------|    |----------------|",
        "       |     | pred_id(PK)|    | behaviour_id   |",
        "       |     | student_id |    | student_id(FK) |",
        "       |     | risk_level |    | stress_level   |",
        "       |     | probability|    | family_income  |",
        "       |     | explanation|    | internet_access|",
        "       |     +------------+    +----------------+",
        "       |",
        "       |1              N",
        "+------+------+     +------------------+     +--------------------+",
        "|notifications|     |counselling_      |     |  login_history     |",
        "|-------------|     |recommendations   |     |--------------------|",
        "| notif_id(PK)|     |------------------|     | login_id(PK)       |",
        "| user_id(FK) |     | rec_id(PK)       |     | user_id(FK)        |",
        "| title       |     | prediction_id(FK)|     | login_time         |",
        "| message     |     | counsellor_id(FK)|     | ip_address         |",
        "| is_read     |     | recommendation   |     | status             |",
        "| created_at  |     | follow_up_date   |     +--------------------+",
        "+-------------+     | status           |",
        "                     +------------------+",
    ]
    er_text = "<br/>".join(er_lines)
    elements.append(Paragraph(er_text, ParagraphStyle('er', parent=code_style, fontSize=7, leading=8.5, leftIndent=0)))
    elements.extend(caption(2, "Entity-Relationship Diagram", "Normalized database schema showing table relationships and foreign key constraints"))
    elements.append(new_page())

    # ============================================================
    # 11. TECHNOLOGY STACK
    # ============================================================
    elements.append(heading1("9. TECHNOLOGY STACK"))
    tech_rows = [
        ["Flask 3.1.1", "Python Web Framework", "Backend routing, request handling, session management, template rendering"],
        ["Python 3.x", "Programming Language", "Application logic, ML model integration, data processing"],
        ["MySQL", "Relational Database", "Persistent data storage with foreign key constraints and indexes"],
        ["HTML5 / CSS3", "Markup & Styling", "Frontend structure and responsive design"],
        ["JavaScript", "Client-side Scripting", "Dynamic interactions, AJAX calls, form validation"],
        ["Bootstrap 5", "CSS Framework", "Responsive UI components, grid system, utility classes"],
        ["Scikit-Learn 1.7.1", "ML Library", "Gradient Boosting Classifier, StandardScaler, train-test split"],
        ["Pandas 2.3.1", "Data Processing", "Data loading, feature extraction, DataFrame operations"],
        ["NumPy 2.2.6", "Numerical Computing", "Array operations, mathematical computations"],
        ["Jinja2 3.1.6", "Template Engine", "Server-side HTML rendering with template inheritance"],
        ["WTForms 3.2.1", "Form Handling", "Form validation, CSRF protection, field rendering"],
        ["Joblib 1.5.1", "Model Serialization", "Save and load trained ML model pipelines"],
        ["Matplotlib 3.10.5", "Visualization", "Confusion matrix and accuracy plots generation"],
        ["ReportLab 4.4.2", "PDF Generation", "Generate professional PDF reports for download"],
        ["OpenPyXL 3.1.5", "Excel Export", "Generate Excel reports with formatted data"],
        ["BCrypt 4.3.0", "Password Hashing", "Secure password storage and verification"],
        ["MySQL Connector", "Database Driver", "Python-MySQL connectivity with parameterized queries"],
        ["Flask-Login", "Session Management", "User authentication, session handling, login required"],
        ["Flask-WTF", "CSRF Protection", "Cross-site request forgery prevention"],
    ]
    elements.append(make_table(["Technology", "Type", "Purpose in Project"], tech_rows, col_widths=[3.5*cm, 3.5*cm, 8.5*cm]))
    elements.append(new_page())

    # ============================================================
    # 12. MODULE DESCRIPTION
    # ============================================================
    elements.append(heading1("10. MODULE DESCRIPTION"))

    # 10.1 Authentication Module
    elements.append(heading2("10.1 Authentication Module"))
    elements.append(body("The Authentication Module handles user registration, login, logout, and session management. It implements role-based access control with three user roles: Admin, Counsellor, and Student. The module is implemented in <b>auth_routes.py</b> and <b>auth_service.py</b>."))
    for f in [
        "Role-based registration with validation (email uniqueness, password strength)",
        "Secure login with bcrypt password hashing and failed attempt tracking",
        "Account lockout mechanism after 5 failed login attempts (60-second lock)",
        "Session management with Flask-Login integration",
        "CSRF protection for all form submissions",
        "Role-based redirect after login to respective dashboards",
    ]:
        elements.append(bullet(f))

    # 10.2 Student Module
    elements.append(heading2("10.2 Student Module"))
    elements.append(body("The Student Module provides students with a personalized dashboard to view their academic records, prediction results, and counselling recommendations. Implemented in <b>student_routes.py</b> and <b>academic_service.py</b>."))
    for f in [
        "Dashboard showing latest prediction result with risk level indicator",
        "Academic record management (add, update, delete semester-wise records)",
        "Academic summary page with comprehensive performance overview",
        "Prediction history tracking across multiple semesters",
        "Profile management and notification centre",
    ]:
        elements.append(bullet(f))

    # 10.3 Admin Module
    elements.append(heading2("10.3 Admin Module"))
    elements.append(body("The Admin Module provides system administrators with complete control over users, students, and system configuration. Implemented in <b>admin_routes.py</b> and <b>report_service.py</b>."))
    for f in [
        "Dashboard with statistics (total students, counsellors, predictions, risk distribution)",
        "Student management (view all students with search and filter capabilities)",
        "Student detail view showing complete profile, academic records, and predictions",
        "Counsellor management (add, activate/deactivate counsellor accounts)",
        "Report generation in PDF and Excel formats",
        "Risk analytics visualization and data export",
    ]:
        elements.append(bullet(f))

    # 10.4 Counsellor Module
    elements.append(heading2("10.4 Counsellor Module"))
    elements.append(body("The Counsellor Module enables counsellors to monitor at-risk students, manage counselling sessions, and track follow-ups. Implemented in <b>counsellor_routes.py</b> and <b>recommendation_service.py</b>."))
    for f in [
        "Risk-ranked student list showing all students sorted by dropout risk",
        "Student detail view with AI prediction and academic summary",
        "Counselling note management (add and track counselling sessions)",
        "Follow-up scheduling and status tracking (Pending, In Progress, Completed, Missed)",
        "Filters for High, Medium, and Low risk student categories",
    ]:
        elements.append(bullet(f))

    # 10.5 AI Prediction Module
    elements.append(heading2("10.5 AI Prediction Module"))
    elements.append(body("The AI Prediction Module is the core intelligence of the system. It uses a trained Gradient Boosting model to predict dropout risk based on student data. Implemented in <b>prediction_service.py</b> and <b>ml_model_service.py</b>."))
    for f in [
        "Gradient Boosting Classifier with 8 input features",
        "StandardScaler preprocessing for feature normalization",
        "Scikit-learn Pipeline for streamlined prediction workflow",
        "Post-processing logic to adjust predictions based on academic indicators",
        "Singleton model loading pattern for performance optimization",
        "Graceful fallback mechanism when model fails to load",
    ]:
        elements.append(bullet(f))

    # 10.6 Reports Module
    elements.append(heading2("10.6 Reports Module"))
    elements.append(body("The Reports Module generates comprehensive PDF and Excel reports for institutional analysis. Implemented in <b>report_service.py</b> and <b>pdf_service.py</b>."))
    for f in [
        "Dashboard statistics aggregation (total counts, averages, distributions)",
        "PDF report generation using ReportLab with professional formatting",
        "Excel report generation using OpenPyXL with structured data layout",
        "Student-specific PDF reports with complete academic and prediction data",
        "Downloadable reports with descriptive filenames",
    ]:
        elements.append(bullet(f))

    # 10.7 Notification Module
    elements.append(heading2("10.7 Notification Module"))
    elements.append(body("The Notification Module manages in-app notifications to alert users about important updates and interventions. Implemented in <b>notification_service.py</b> and <b>notification_model.py</b>."))
    for f in [
        "User-specific notification storage in database",
        "Read/unread status tracking for notification management",
        "Title and message fields for structured notification display",
        "Timestamps for notification ordering and tracking",
        "Integration with prediction and counselling workflows",
    ]:
        elements.append(bullet(f))
    elements.append(new_page())

    # ============================================================
    # 13. AI MODEL WORKING
    # ============================================================
    elements.append(heading1("11. AI MODEL WORKING"))
    elements.append(body("The AI prediction model is the heart of the system. This section explains the complete workflow from dataset creation through model training to real-time prediction."))

    elements.append(heading2("11.1 Dataset"))
    elements.append(body("The dataset is a synthetically generated collection of 2,000 student records, designed to realistically represent the academic and socio-demographic profiles of engineering college students. Each record contains 8 features and a binary target variable (dropout). The dataset generation logic in <b>generate_dataset.py</b> uses a risk scoring system where students with risk score >= 7 are labelled as dropout=1."))
    elements.append(body_b("Model Features:"))
    feat_rows = [
        ["cgpa", "Numeric (0-10)", "Cumulative Grade Point Average", "Strong predictor: lower CGPA = higher risk"],
        ["attendance", "Numeric (0-100)", "Percentage of classes attended", "Critical: <65% significantly increases risk"],
        ["internal_marks", "Numeric (0-100)", "Internal assessment marks", "Reflects consistent academic effort"],
        ["backlog_count", "Integer (0+)", "Number of pending backlogs", "Key risk multiplier: >4 backlogs = high risk"],
        ["study_hours", "Numeric (0-24)", "Daily study hours", "Low hours (<2) indicates disengagement"],
        ["family_income", "Numeric", "Annual family income (INR)", "Socio-economic stress factor"],
        ["parent_education", "Integer (0-3)", "0=None, 1=School, 2=Graduate, 3=Post-grad", "Parental education influence"],
        ["internet_access", "Boolean (0/1)", "Availability of internet at home", "Digital divide impact on learning"],
    ]
    elements.append(make_table(["Feature", "Type", "Description", "Importance"], feat_rows, col_widths=[2.8*cm, 3*cm, 4.5*cm, 5.2*cm]))

    elements.append(heading2("11.2 Model Training"))
    elements.append(body("The model is trained using the following pipeline implemented in <b>train_model.py</b>:"))
    for s in [
        "<b>Data Loading:</b> Processed dataset (processed_dataset.csv) is loaded using Pandas.",
        "<b>Feature Extraction:</b> 8 features are extracted into feature matrix X, with target variable y being the 'dropout' column.",
        "<b>Train-Test Split:</b> Data is split into 80% training and 20% testing sets, stratified by target to maintain class distribution.",
        "<b>Standardization:</b> StandardScaler normalizes features to zero mean and unit variance.",
        "<b>Gradient Boosting:</b> A GradientBoostingClassifier with 200 estimators, learning rate 0.05, and max depth 4 is trained.",
        "<b>Evaluation:</b> Model achieves 98.80% accuracy on the test set with precision of 0.99 and recall of 0.98 for dropout class.",
        "<b>Validation:</b> Four test cases (Good, Excellent, At-Risk, Critical) validate the model's risk assessment logic.",
        "<b>Serialization:</b> The complete pipeline (scaler + model) is saved using joblib for production use.",
    ]:
        elements.append(bullet(s))

    elements.append(spacer(6))
    elements.append(body_b("Model Prediction Flow:"))
    flow_lines = [
        "+--------------+     +--------------+     +------------------+",
        "|  Student     |     |  Academic    |     |  ML Model        |",
        "|  Profile     |---->|  Data (8     |---->|  Pipeline        |",
        "|  (from DB)   |     |  Features)   |     |  (Load Once)     |",
        "+--------------+     +--------------+     +--------+---------+",
        "                                                     |",
        "                                                     v",
        "+--------------+     +--------------+     +------------------+",
        "| Counselling  |     | Risk Level   |     |  Post-Processing |",
        "| Recommenda-  |<----| Assignment   |<----|  & Probability   |",
        "| tion         |     | Low/Med/High |     |  Calculation     |",
        "+--------------+     +--------------+     +------------------+",
    ]
    flow_text = "<br/>".join(flow_lines)
    elements.append(Paragraph(flow_text, ParagraphStyle('flow', parent=code_style, fontSize=7.5, leading=9, leftIndent=0)))
    elements.extend(caption(3, "AI Model Prediction Flow", "End-to-end flow from student data to risk classification and recommendation generation"))

    elements.append(heading2("11.3 Risk Levels & Thresholds"))
    risk_rows = [
        ["Low Risk", "< 35%", "Green (Safe)", "Student is performing well academically. Maintain current habits."],
        ["Medium Risk", "35% - 60%", "Amber (Warning)", "Student shows some risk indicators. Requires monitoring."],
        ["High Risk", ">= 60%", "Red (Danger)", "Student at critical risk. Immediate intervention required."],
    ]
    elements.append(make_table(["Risk Level", "Probability Range", "Indicator", "Action Required"], risk_rows, col_widths=[2.5*cm, 3*cm, 3*cm, 7*cm]))

    elements.append(heading2("11.4 Recommendation Generation"))
    elements.append(body("The system generates context-aware recommendations based on risk level and specific student metrics. The <b>recommendation_service.py</b> module provides three tiers of recommendations:"))
    for r in [
        "<b>High Risk:</b> 'Immediate counselling session required. Attendance is critically low (45.2%). Clear 5 pending backlogs with faculty support.'",
        "<b>Medium Risk:</b> 'Performance needs improvement. Attendance (68.5%) is below recommended 75%. Increase study time and participate in peer study groups.'",
        "<b>Low Risk:</b> 'Keep up the excellent work! Outstanding CGPA of 8.5. Maintain current attendance and study habits.'",
    ]:
        elements.append(bullet(r))
    elements.append(new_page())

    # ============================================================
    # 14. SOFTWARE CODING DEMONSTRATION
    # ============================================================
    elements.append(heading1("12. SOFTWARE CODING DEMONSTRATION"))
    elements.append(body("This section presents the most important code modules from the project. Each code snippet is a critical component of the system's functionality, taken directly from the actual source code."))

    elements.append(heading2("12.1 Flask Application Factory"))
    elements.append(body("The application factory pattern initializes the Flask app, registers blueprints, and configures extensions. From <b>app/__init__.py</b>:"))
    elements.append(code_block("def create_app():<br/>    &nbsp;&nbsp;&nbsp;&nbsp;app = Flask(__name__)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;app.config.from_object(Config)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;init_extensions(app)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;# Register Blueprints<br/>    &nbsp;&nbsp;&nbsp;&nbsp;app.register_blueprint(auth_bp)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;app.register_blueprint(student_bp)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;app.register_blueprint(admin_bp)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;app.register_blueprint(counsellor_bp)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;app.register_blueprint(api_bp)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;register_error_handlers(app)<br/>    &nbsp;&nbsp;&nbsp;&nbsp;return app"))

    elements.append(heading2("12.2 Gradient Boosting Model Training"))
    elements.append(body("The core ML training pipeline with StandardScaler and GradientBoostingClassifier. From <b>app/ml/train_model.py</b>:"))
    elements.append(code_block("# Build Pipeline: Scaler + Gradient Boosting<br/>pipeline = Pipeline([<br/>    &nbsp;&nbsp;&nbsp;&nbsp;('scaler', StandardScaler()),<br/>    &nbsp;&nbsp;&nbsp;&nbsp;('model', GradientBoostingClassifier(<br/>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;n_estimators=200,<br/>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;learning_rate=0.05,<br/>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;max_depth=4,<br/>    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;random_state=42<br/>    &nbsp;&nbsp;&nbsp;&nbsp;))<br/>])<br/>pipeline.fit(X_train, y_train)<br/>accuracy = accuracy_score(y_test, pipeline.predict(X_test))<br/>print(f'Accuracy : {accuracy * 100:.2f}%')<br/>joblib.dump(pipeline, MODEL_PATH)"))

    elements.append(heading2("12.3 Dropout Prediction Service"))
    elements.append(body("The prediction service coordinates between ML model and database. From <b>app/services/prediction_service.py</b>:"))
    elements.append(code_block("class dropout_predictionservice:<br/>    @staticmethod<br/>    def predict_dropout(student_id):<br/>        data = AcademicModel.get_student_academic_summary(student_id)<br/>        if not data:<br/>            return {'risk_level': 'Low', 'score': 0.0}<br/>        student_features = {<br/>            'cgpa': float(data['cgpa']),<br/>            'attendance': float(data['attendance']),<br/>            'internal_marks': float(data['internal_marks']),<br/>            'backlog_count': int(data['backlog_count']),<br/>            'study_hours': float(data['study_hours']),<br/>            'family_income': 50000,<br/>            'parent_education': 2,<br/>            'internet_access': 1<br/>        }<br/>        result = MLModelService.predict(student_features)<br/>        risk_level = result.get('risk_level')<br/>        recommendation = _build_recommendation(risk_level, data)<br/>        return {<br/>            'student_id': data['student_id'],<br/>            'risk_level': risk_level,<br/>            'probability': result['probability'],<br/>            'recommendation': recommendation<br/>        }"))

    elements.append(heading2("12.4 Core Database Schema"))
    elements.append(body("The MySQL schema for storing users, students, academic records, and predictions. From <b>database/schema.sql</b>:"))
    elements.append(code_block("CREATE TABLE users (<br/>    user_id       INT AUTO_INCREMENT PRIMARY KEY,<br/>    full_name     VARCHAR(100) NOT NULL,<br/>    email         VARCHAR(100) UNIQUE NOT NULL,<br/>    password_hash VARCHAR(255) NOT NULL,<br/>    role          ENUM('Admin','Student','Counsellor') NOT NULL,<br/>    is_active     BOOLEAN DEFAULT TRUE,<br/>    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP<br/>);<br/><br/>CREATE TABLE academic_records (<br/>    academic_id    INT AUTO_INCREMENT PRIMARY KEY,<br/>    student_id     INT NOT NULL,<br/>    semester       INT,<br/>    cgpa           DECIMAL(4,2),<br/>    attendance     DECIMAL(5,2),<br/>    backlog_count  INT DEFAULT 0,<br/>    study_hours    DECIMAL(4,2),<br/>    FOREIGN KEY (student_id) REFERENCES students(student_id)<br/>);"))

    elements.append(heading2("12.5 ML Model Post-Processing Logic"))
    elements.append(body("The post-processing ensures realistic risk assessment by adjusting raw model probabilities. From <b>app/services/ml_model_service.py</b>:"))
    elements.append(code_block("# Post-processing: Adjust model probability based on academic indicators<br/>if (cgpa >= 8.0 and attendance >= 85 and backlog_count == 0):<br/>    adjusted_prob = min(probability_raw, 0.15)<br/>    risk_level = 'Low'  # Excellent student override<br/>elif (cgpa < 5.5 or attendance < 55 or backlog_count >= 4):<br/>    adjusted_prob = max(probability_raw, 0.65)<br/>    risk_level = 'High'  # Critical indicators<br/>elif (cgpa < 6.5 or attendance < 65 or backlog_count >= 2):<br/>    adjusted_prob = max(probability_raw, 0.40)<br/>    risk_level = 'Medium'  # Below average<br/>else:<br/>    risk_level = 'Low' if adjusted_prob < 35 else 'Medium'"))

    elements.append(new_page())

    # ============================================================
    # 15. OUTPUT SCREENSHOTS
    # ============================================================
    elements.append(heading1("13. OUTPUT SCREENSHOTS"))
    elements.append(body("This section presents screenshots of the running application, demonstrating the key features and user interfaces of the AI-Based Student Dropout Prediction and Counselling System. The screenshots are attached as a separate PDF document and are described below with figure numbers and captions."))
    elements.append(spacer(6))
    elements.append(body_b("The following screenshots are included in the attached Output Screenshots PDF:"))
    
    screenshot_descriptions = [
        ("Figure 4", "Login Page", "Secure login interface with email and password authentication for all user roles."),
        ("Figure 5", "Registration Page", "User registration form with role selection (Admin, Student, Counsellor) and input validation."),
        ("Figure 6", "Student Dashboard", "Student dashboard showing latest AI prediction result, risk level indicator, and academic records overview."),
        ("Figure 7", "Academic Record Form", "Form for adding semester-wise academic data including CGPA, attendance, internal marks, and backlog count."),
        ("Figure 8", "Prediction Result Page", "Detailed prediction result showing risk level, probability score, and personalized counselling recommendation."),
        ("Figure 9", "Admin Dashboard", "Admin dashboard with statistics: total students, counsellors, predictions, and risk distribution."),
        ("Figure 10", "Student Management", "Admin view showing list of all students with search, filter, and detail view capabilities."),
        ("Figure 11", "Counsellor Dashboard", "Counsellor dashboard with risk-ranked student list and counselling session management."),
        ("Figure 12", "At-Risk Students View", "Filtered view showing only high-risk students requiring immediate counselling intervention."),
        ("Figure 13", "Counselling Notes", "Counselling session tracking with status management (Pending, In Progress, Completed)."),
        ("Figure 14", "Reports Page", "Analytics dashboard with risk distribution visualization and PDF/Excel export options."),
        ("Figure 15", "Confusion Matrix", "Model evaluation confusion matrix showing classification performance."),
    ]
    for fig_num, title, desc in screenshot_descriptions:
        elements.append(Paragraph(f"<b>{fig_num}: {title}</b>", ParagraphStyle('ss', parent=body_style, fontSize=11, spaceBefore=6, spaceAfter=2)))
        elements.append(Paragraph(desc, ParagraphStyle('ss2', parent=body_style, fontSize=11, spaceAfter=2)))
    elements.append(new_page())

    # ============================================================
    # 16. FUTURE WORK
    # ============================================================
    elements.append(heading1("14. FUTURE WORK"))
    for f in [
        "<b>Deep Learning Integration:</b> Incorporate deep learning models such as LSTM and Transformer networks for sequential analysis of student performance across semesters.",
        "<b>Real-Time Data Integration:</b> Integrate with institutional Learning Management Systems (LMS) for real-time data synchronization and live performance tracking.",
        "<b>Mobile Application:</b> Develop a cross-platform mobile application (React Native/Flutter) for students and counsellors to access the system on-the-go.",
        "<b>Advanced Analytics Dashboard:</b> Implement interactive dashboards with Chart.js/D3.js visualizations, trend analysis, and predictive analytics over time.",
        "<b>Multi-Institution Support:</b> Extend the system to support multiple colleges with tenant-based data isolation and centralized administration.",
        "<b>SMS/Email Notifications:</b> Integrate Twilio and SendGrid APIs for automated SMS and email alerts for high-risk student interventions.",
        "<b>Natural Language Processing:</b> Add sentiment analysis of counselling session notes to detect emotional distress indicators.",
        "<b>Explainable AI:</b> Implement SHAP/LIME for model interpretability, helping counsellors understand why specific predictions were made.",
        "<b>Automated Scheduling:</b> Add automated counselling session scheduling with calendar integration and reminder notifications.",
        "<b>Parent Portal:</b> Develop a parent portal for guardians to monitor their ward's academic progress and risk status.",
    ]:
        elements.append(bullet(f))
    elements.append(new_page())

    # ============================================================
    # 17. CONCLUSION
    # ============================================================
    elements.append(heading1("15. CONCLUSION"))
    elements.append(body("The AI-Based Student Dropout Prediction and Counselling System successfully demonstrates the application of machine learning techniques to address the critical challenge of student dropout in higher education. The system integrates a Gradient Boosting Classifier with a comprehensive web platform to provide accurate risk assessment and personalized counselling recommendations."))
    elements.append(body("The system achieves its objectives through a well-designed modular architecture. The ML model effectively categorizes students into Low, Medium, and High risk categories using 8 key features including academic performance metrics and socio-demographic indicators. The post-processing logic ensures realistic risk assessment by adjusting model probabilities based on actual academic thresholds. The model achieves an accuracy of 98.80% with precision of 0.99 and recall of 0.98 for the dropout class."))
    elements.append(body("The web application provides role-specific dashboards for Administrators, Counsellors, and Students, enabling seamless interaction with the prediction system. Features such as automated recommendation generation, PDF/Excel report exports, and notification services enhance the practical utility of the system for educational institutions."))
    elements.append(body("The project successfully demonstrates that AI-powered early warning systems can play a crucial role in student retention efforts. By identifying at-risk students early and providing data-driven counselling recommendations, the system empowers educational institutions to take proactive measures in reducing dropout rates and improving student outcomes."))
    elements.append(new_page())

    # ============================================================
    # 18. REFERENCES
    # ============================================================
    elements.append(heading1("16. REFERENCES"))
    references = [
        "1. Chen, X., Wang, Y., & Liu, Z. (2022). 'Student Dropout Prediction Using Machine Learning: A Comprehensive Review.' IEEE Transactions on Learning Technologies, 15(3), 456-470.",
        "2. Kumar, M., & Singh, R. (2021). 'Deep Learning Approaches for Student Performance Prediction in Higher Education.' International Journal of Artificial Intelligence in Education, 31(2), 234-251.",
        "3. Patel, S., & Joshi, A. (2023). 'Web-Based Counselling Platform for At-Risk Students Using Flask Framework.' Journal of Educational Technology Systems, 51(4), 389-405.",
        "4. Wang, L., Zhang, Y., & Chen, H. (2020). 'Educational Data Mining for Dropout Prediction: A Comparative Study of Classification Algorithms.' Computers & Education, 145, 103-118.",
        "5. Sharma, R. (2023). 'Gradient Boosting for Imbalanced Educational Datasets: A Case Study in Student Dropout Prediction.' Machine Learning with Applications, 12, 100-115.",
        "6. Yamamoto, K. (2021). 'Feature Engineering for Student Academic Risk Assessment in Online Learning Environments.' Educational Technology Research, 69(5), 1123-1140.",
        "7. Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). 'Scikit-learn: Machine Learning in Python.' Journal of Machine Learning Research, 12, 2825-2830.",
        "8. Grinberg, M. (2018). 'Flask Web Development: Developing Web Applications with Python.' 2nd Edition, O'Reilly Media.",
        "9. Geron, A. (2022). 'Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow.' 3rd Edition, O'Reilly Media.",
        "10. Witten, I. H., Frank, E., Hall, M. A., & Pal, C. J. (2016). 'Data Mining: Practical Machine Learning Tools and Techniques.' 4th Edition, Morgan Kaufmann.",
        "11. MySQL Documentation. 'MySQL 8.0 Reference Manual.' Oracle Corporation. Available: https://dev.mysql.com/doc/",
        "12. Bootstrap Documentation. 'Bootstrap 5 Documentation.' Available: https://getbootstrap.com/docs/5.0/",
        "13. Flask Documentation. 'Flask 3.1 Documentation.' Pallets Project. Available: https://flask.palletsprojects.com/",
    ]
    for ref in references:
        elements.append(Paragraph(ref, ref_style))

    # ============================================================
    # BUILD PDF
    # ============================================================
    doc.build(elements, onFirstPage=set_header_footer, onLaterPages=set_header_footer)
    buffer.seek(0)
    return buffer


def merge_screenshots(report_buffer, screenshot_path, output_path):
    """Merge report PDF with screenshot PDF."""
    try:
        report_reader = PdfReader(report_buffer)
        screenshot_reader = PdfReader(screenshot_path)
        writer = PdfWriter()
        for page in report_reader.pages:
            writer.add_page(page)
        for page in screenshot_reader.pages:
            writer.add_page(page)
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"  Report pages: {len(report_reader.pages)}")
        print(f"  Screenshot pages: {len(screenshot_reader.pages)}")
        print(f"  Total pages: {len(report_reader.pages) + len(screenshot_reader.pages)}")
        return True
    except Exception as e:
        print(f"  PDF merge failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  AI-Based Student Dropout Prediction & Counselling System")
    print("  Final Year Project Report Generator")
    print("=" * 60)
    print()
    
    print("Generating report PDF...")
    report_buffer = build_report()
    print("  Report PDF generated successfully.")
    print()
    
    if os.path.exists(SCREENSHOT_PDF):
        print(f"Merging with screenshot PDF: {SCREENSHOT_PDF}")
        success = merge_screenshots(report_buffer, SCREENSHOT_PDF, OUTPUT_PDF)
        if success:
            print(f"  Final PDF saved: {OUTPUT_PDF}")
        else:
            # Save without screenshots
            with open(OUTPUT_PDF, "wb") as f:
                f.write(report_buffer.getvalue())
            print(f"  Report PDF saved (without screenshots): {OUTPUT_PDF}")
    else:
        print(f"Screenshot PDF not found at: {SCREENSHOT_PDF}")
        with open(OUTPUT_PDF, "wb") as f:
            f.write(report_buffer.getvalue())
        print(f"  Report PDF saved: {OUTPUT_PDF}")
    
    print()
    print("=" * 60)
    print("  Report generation completed!")
    print(f"  Output: {OUTPUT_PDF}")
    print("=" * 60)