"""
=============================================================================
AI-Based Student Dropout Prediction & Counselling System
Final Year Project Report - Professional PDF Generator (v2)
-----------------------------------------------------------------------------
Generates: output_report/Final_Project_Report.pdf (~26 pages)
Uses ReportLab for professional PDF with vector diagrams.
=============================================================================
"""
import os, io, math
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
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle
from reportlab.graphics import renderPDF

OUTPUT_DIR = "output_report"
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "Final_Project_Report.pdf")
SCREENSHOT_PDF = os.path.join(OUTPUT_DIR, "screenshots.pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors
NAVY      = colors.HexColor("#1B3A5C")
DARK_BLUE = colors.HexColor("#1e3a8a")
MED_BLUE  = colors.HexColor("#2563eb")
LIGHT_BLUE = colors.HexColor("#dbeafe")
ALT_ROW   = colors.HexColor("#e8edf2")
DARK_TEXT  = colors.HexColor("#1e293b")
GRAY_TEXT  = colors.HexColor("#475569")
BORDER_CLR = colors.HexColor("#cbd5e1")

PAGE_W, PAGE_H = A4

# ============================================================
# STYLES
# ============================================================
styles = getSampleStyleSheet()

title_style = ParagraphStyle('T1', fontName='Times-Bold', fontSize=26, leading=32, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8)
subtitle_style = ParagraphStyle('T2', fontName='Times-Roman', fontSize=14, leading=18, textColor=DARK_TEXT, alignment=TA_CENTER, spaceAfter=4)
h1_style = ParagraphStyle('H1', fontName='Times-Bold', fontSize=15, leading=20, textColor=colors.white, spaceBefore=0, spaceAfter=0, borderWidth=0)
h1_bg = colors.HexColor("#1B3A5C")
h2_style = ParagraphStyle('H2', fontName='Times-Bold', fontSize=13, leading=17, textColor=DARK_BLUE, spaceBefore=10, spaceAfter=5)
body_style = ParagraphStyle('B', fontName='Times-Roman', fontSize=12, leading=18, textColor=DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=5)
bullet_style = ParagraphStyle('BL', fontName='Times-Roman', fontSize=12, leading=17, textColor=DARK_TEXT, leftIndent=18, bulletIndent=6, spaceBefore=1, spaceAfter=1)
code_style = ParagraphStyle('CD', fontName='Courier', fontSize=8, leading=10, textColor=DARK_TEXT, leftIndent=8, spaceBefore=3, spaceAfter=3, backColor=colors.HexColor("#f8fafc"), borderColor=BORDER_CLR, borderWidth=0.5, borderPadding=4)
caption_style = ParagraphStyle('CP', fontName='Times-Bold', fontSize=10, leading=14, textColor=DARK_TEXT, alignment=TA_CENTER, spaceBefore=3, spaceAfter=1)
cap_sub_style = ParagraphStyle('CS', fontName='Times-Italic', fontSize=9, leading=12, textColor=GRAY_TEXT, alignment=TA_CENTER, spaceBefore=0, spaceAfter=6)
toc_hdr = ParagraphStyle('TH', fontName='Times-Bold', fontSize=11, leading=15, textColor=colors.white, alignment=TA_CENTER)
toc_cell = ParagraphStyle('TC', fontName='Times-Roman', fontSize=11, leading=16, textColor=DARK_TEXT)
toc_cen = ParagraphStyle('TCC', parent=toc_cell, alignment=TA_CENTER)
tb_hdr = ParagraphStyle('TBH', fontName='Times-Bold', fontSize=9.5, leading=13, textColor=colors.white, alignment=TA_CENTER)
tb_cell = ParagraphStyle('TBC', fontName='Times-Roman', fontSize=9.5, leading=13, textColor=DARK_TEXT, alignment=TA_CENTER)
tb_left = ParagraphStyle('TBL', parent=tb_cell, alignment=TA_LEFT)
ref_style = ParagraphStyle('RF', fontName='Times-Roman', fontSize=11, leading=15, textColor=DARK_TEXT, spaceAfter=3)

# ============================================================
# HEADER/FOOTER
# ============================================================
def set_hf(canvas_obj, doc):
    canvas_obj.saveState()
    # Top
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, PAGE_H - 16, PAGE_W, 16, stroke=0, fill=1)
    canvas_obj.setFont("Times-Bold", 9)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.drawString(28, PAGE_H - 12, "AI-Based Student Dropout Prediction & Counselling System")
    # Bottom
    canvas_obj.setFillColor(MED_BLUE)
    canvas_obj.rect(0, 0, PAGE_W, 10, stroke=0, fill=1)
    canvas_obj.setFont("Times-Italic", 8)
    canvas_obj.setFillColor(colors.white)
    canvas_obj.drawString(28, 2, "Confidential - Final Year Project Report | VSB Engineering College")
    canvas_obj.drawRightString(PAGE_W - 28, 2, f"Page {doc.page}")
    canvas_obj.restoreState()

# ============================================================
# HELPERS
# ============================================================
def h1(text):
    """Styled heading 1 with background bar."""
    t = Paragraph(f"<b>{text}</b>", h1_style)
    data = [[t]]
    tbl = Table(data, colWidths=[15.5*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), h1_bg),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return tbl

def h2(text):
    return Paragraph(f"<b>{text}</b>", h2_style)

def body(text):
    return Paragraph(text, body_style)

def bullet(text):
    return Paragraph(f"•  {text}", bullet_style)

def code(text):
    return Paragraph(text.replace('\n','<br/>'), code_style)

def fig_cap(num, title, sub=""):
    e = [Paragraph(f"<b>Figure {num}:</b> {title}", caption_style)]
    if sub:
        e.append(Paragraph(sub, cap_sub_style))
    return e

def tbl_cap(num, title):
    return Paragraph(f"<b>Table {num}:</b> {title}", caption_style)

def make_table(headers, rows, col_widths=None):
    h = [Paragraph(h, tb_hdr) for h in headers]
    data = [h]
    for r in rows:
        row = []
        for i, c in enumerate(r):
            st = tb_left if i == 0 else tb_cell
            row.append(Paragraph(str(c), st))
        data.append(row)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    s = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            s.append(('BACKGROUND', (0,i), (-1,i), ALT_ROW))
    t.setStyle(TableStyle(s))
    return t

def sp(h=4):
    return Spacer(1, h)

def new_page():
    return PageBreak()

# ============================================================
# ARCHITECTURE DIAGRAM (Vector Drawing)
# ============================================================
class ArchitectureDiagram(Flowable):
    def __init__(self):
        Flowable.__init__(self)
        self.width = 480
        self.height = 240
    
    def draw(self):
        c = self.canv
        # Layer definitions
        layers = [
            ("PRESENTATION LAYER", 0, [("Admin Dashboard", "#3b82f6"), ("Counsellor Dashboard", "#10b981"), ("Student Dashboard", "#f59e0b"), ("HTML/CSS/JS Templates", "#6366f1")]),
            ("APPLICATION LAYER (Flask)", 1, [("Auth Routes/Services", "#8b5cf6"), ("Student Routes/Services", "#ec4899"), ("Admin Routes/Services", "#ef4444"), ("Counsellor Routes", "#14b8a6")]),
            ("ML LAYER (Scikit-Learn)", 2, [("Gradient Boosting", "#f97316"), ("Standard Scaler", "#06b6d4"), ("Pipeline Manager", "#84cc16")]),
            ("DATA LAYER (MySQL)", 3, [("Users/Students", "#1d4ed8"), ("Academic Records", "#047857"), ("Predictions/Notes", "#b91c1c"), ("Notifications/Logs", "#6d28d9")]),
        ]
        
        bar_h = 40
        gap = 12
        box_w = 100
        box_h = 26
        y_start = self.height - 12
        
        for layer_idx, (layer_name, layer_num, boxes) in enumerate(layers):
            y = y_start - layer_idx * (bar_h + gap)
            
            # Layer background
            c.setFillColor(colors.HexColor("#f1f5f9"))
            c.setStrokeColor(NAVY)
            c.setLineWidth(1)
            c.roundRect(0, y - box_h, self.width, bar_h, 4, stroke=1, fill=1)
            
            # Layer title
            c.setFont("Times-Bold", 8)
            c.setFillColor(NAVY)
            c.drawString(8, y - box_h + 14, layer_name)
            
            # Draw arrow connections between layers
            if layer_idx < len(layers) - 1:
                ny = y - box_h - gap
                c.setStrokeColor(MED_BLUE)
                c.setLineWidth(1.5)
                cx = self.width / 2
                c.line(cx, y - box_h, cx, ny + bar_h)
                # Arrow head
                c.setFillColor(MED_BLUE)
                c.drawPolygon([cx-4, ny+bar_h-1, cx+4, ny+bar_h-1, cx, ny+bar_h+5], fill=1, stroke=0)
            
            # Draw boxes
            total_boxes = len(boxes)
            box_area_w = self.width - 120  # space for layer title
            box_gap = 8
            box_total_w = total_boxes * box_w + (total_boxes - 1) * box_gap
            box_start_x = 120 + (box_area_w - box_total_w) / 2
            
            for bi, (bname, bcolor) in enumerate(boxes):
                bx = box_start_x + bi * (box_w + box_gap)
                by = y - box_h + 5
                bc = colors.HexColor(bcolor)
                c.setFillColor(bc)
                c.setStrokeColor(colors.HexColor("#cbd5e1"))
                c.setLineWidth(0.5)
                c.roundRect(bx, by, box_w, box_h - 10, 3, stroke=1, fill=1)
                c.setFont("Times-Roman", 7)
                c.setFillColor(colors.white)
                c.drawCentredString(bx + box_w/2, by + 6, bname[:22])

# ============================================================
# ER DIAGRAM (Vector Drawing)
# ============================================================
class ERDiagram(Flowable):
    def __init__(self):
        Flowable.__init__(self)
        self.width = 480
        self.height = 270
    
    def draw(self):
        c = self.canv
        
        # Entity boxes: (x, y, w, h, name, columns)
        entities = [
            (180, 220, 120, 40, "users", "user_id (PK), full_name, email,\npassword_hash, role, phone,\nis_active, created_at"),
            (20, 120, 120, 40, "students", "student_id (PK),\nuser_id (FK), roll_no,\ndepartment, year_of_study,\ngender, date_of_birth, address"),
            (200, 40, 120, 40, "academic_records", "academic_id (PK),\nstudent_id (FK), semester,\ncgpa, attendance,\ninternal_marks, backlog_count,\nstudy_hours"),
            (350, 120, 125, 40, "dropout_predictions", "prediction_id (PK),\nstudent_id (FK),\nrisk_level, probability,\nexplanation, model_version,\npredicted_on"),
            (370, 200, 100, 35, "notifications", "notif_id (PK),\nuser_id (FK), title,\nmessage, is_read,\ncreated_at"),
        ]
        
        # Relationships: (x1, y1, x2, y2, label)
        rels = [
            (180+60, 220, 20+60, 160, "1:1"),
            (20+60, 120, 200+40, 80, "1:N"),
            (180+60, 220, 350+40, 165, "1:N"),
            (180+60, 220, 370+25, 200, "1:N"),
            (200+60, 40, 350+40, 120, "1:N"),
        ]
        
        for (x, y, w, h, name, cols), (rx1, ry1, rx2, ry2, rlab) in zip(entities, rels):
            # Entity rect
            c.setFillColor(colors.white)
            c.setStrokeColor(NAVY)
            c.setLineWidth(1.5)
            c.roundRect(x, y-h, w, h, 5, stroke=1, fill=1)
            
            # Title bar
            c.setFillColor(DARK_BLUE)
            c.roundRect(x, y-h+26, w, h-26, 5, stroke=0, fill=1)
            c.roundRect(x, y-h+26, w, 14, 5, stroke=0, fill=0)
            c.setFillColor(DARK_BLUE)
            c.rect(x, y-h+12, w, 14, stroke=0, fill=1)
            
            # Name
            c.setFont("Times-Bold", 9)
            c.setFillColor(colors.white)
            c.drawCentredString(x + w/2, y - h + 15, name.replace("_", " "))
            
            # Columns
            c.setFont("Courier", 6.5)
            c.setFillColor(DARK_TEXT)
            lines = cols.split("\n")
            for li, line in enumerate(lines):
                c.drawString(x + 6, y - h + 38 - li*9, line)
            
            # Relationship line
            c.setStrokeColor(MED_BLUE)
            c.setLineWidth(1.2)
            c.line(rx1, ry1, rx2, ry2)
            # Label
            c.setFont("Times-Italic", 8)
            c.setFillColor(NAVY)
            mx, my = (rx1+rx2)/2, (ry1+ry2)/2
            c.drawCentredString(mx, my-8, rlab)

# ============================================================
# BUILD REPORT
# ============================================================
def build_report():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        topMargin=1.6*cm, bottomMargin=1.4*cm,
        leftMargin=2.2*cm, rightMargin=2.2*cm)
    e = []  # elements
    
    # ════════════════════════════════════════════════════════
    # 1. TITLE PAGE
    # ════════════════════════════════════════════════════════
    e.append(sp(80))
    e.append(Paragraph("AI-Based Student Dropout Prediction<br/>& Counselling System", ParagraphStyle('TP', fontName='Times-Bold', fontSize=24, leading=30, textColor=NAVY, alignment=TA_CENTER)))
    e.append(sp(20))
    e.append(Paragraph("<i>A Project Report</i>", subtitle_style))
    e.append(Paragraph("submitted in partial fulfillment of the requirements<br/>for the award of the degree of", ParagraphStyle('TMP', fontName='Times-Italic', fontSize=12, leading=16, alignment=TA_CENTER, textColor=DARK_TEXT)))
    e.append(sp(12))
    e.append(Paragraph("<b>Bachelor of Engineering in<br/>Artificial Intelligence and Machine Learning</b>", ParagraphStyle('TMP2', fontName='Times-Bold', fontSize=14, leading=18, textColor=DARK_TEXT, alignment=TA_CENTER)))
    e.append(sp(12))
    e.append(Paragraph("Submitted by", ParagraphStyle('TMP3', fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, textColor=DARK_TEXT)))
    e.append(sp(4))
    e.append(Paragraph("<b>Sabarish S<br/>Register Number: 922524148094</b>", ParagraphStyle('TMP4', fontName='Times-Bold', fontSize=14, leading=18, textColor=NAVY, alignment=TA_CENTER)))
    e.append(sp(30))
    e.append(Paragraph("<b>VSB Engineering College<br/>III Year<br/>2025 – 2026</b>", ParagraphStyle('TMP5', fontName='Times-Bold', fontSize=14, leading=18, textColor=NAVY, alignment=TA_CENTER)))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 2. ABSTRACT + TOC
    # ════════════════════════════════════════════════════════
    e.append(h1("ABSTRACT"))
    e.append(body("Student dropout is a critical challenge in higher education. This project presents an AI-Based Student Dropout Prediction and Counselling System that leverages machine learning to predict dropout risk and provide personalized counselling recommendations."))
    e.append(body("The system employs a <b>Gradient Boosting Classifier</b> trained on 8 features: CGPA, attendance, internal marks, backlog count, study hours, family income, parent education, and internet access. The model achieves <b>98.80% accuracy</b> in categorizing students into Low, Medium, and High risk categories. A Flask web application provides role-specific dashboards for Administrators, Counsellors, and Students."))
    e.append(body("Key features include real-time prediction, automated recommendations, academic record management, counselling tracking, PDF/Excel reports, and notification services. Built with Python, Flask, MySQL, and Scikit-Learn, the system follows a modular architecture ensuring scalability and maintainability."))
    
    # TOC on same page if space permits
    e.append(h1("TABLE OF CONTENTS"))
    toc_items = [
        ("1.", "Abstract"), ("2.", "Objectives"), ("3.", "Scope of the Project"),
        ("4.", "Literature Survey"), ("5.", "Existing System"), ("6.", "Proposed System"),
        ("7.", "System Architecture"), ("8.", "Database Design"), ("9.", "Technology Stack"),
        ("10.", "Module Description"), ("11.", "AI Model Working"), ("12.", "Software Coding Demonstration"),
        ("13.", "Output Screenshots"), ("14.", "Future Work"), ("15.", "Conclusion"), ("16.", "References"),
    ]
    toc_data = [[Paragraph("<b>S.No</b>", toc_hdr), Paragraph("<b>Description</b>", toc_hdr)]]
    for sno, title in toc_items:
        toc_data.append([Paragraph(sno, toc_cen), Paragraph(title, toc_cell)])
    tt = Table(toc_data, colWidths=[1.5*cm, 13.5*cm], repeatRows=1)
    ts = [('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
          ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
          ('GRID',(0,0),(-1,-1),0.5,BORDER_CLR),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]
    for i in range(1,len(toc_data)):
        if i%2==0:
            ts.append(('BACKGROUND',(0,i),(-1,i),ALT_ROW))
    tt.setStyle(TableStyle(ts))
    e.append(tt)
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 3. OBJECTIVES + SCOPE
    # ════════════════════════════════════════════════════════
    e.append(h1("2. OBJECTIVES"))
    objs = [
        "<b>Primary Objective:</b> Develop an AI web application for accurate dropout prediction using ML, enabling early intervention.",
        "<b>Early Risk Identification:</b> Identify at-risk students at the earliest stage using academic and behavioural indicators.",
        "<b>Automated Recommendations:</b> Generate personalized counselling recommendations based on risk level and individual factors.",
        "<b>Multi-Role Dashboard:</b> Create role-specific interfaces for Admin, Counsellors, and Students with access controls.",
        "<b>Data Management:</b> Centralize student records, academic data, behaviour data, counselling notes, and predictions.",
        "<b>Report Generation:</b> Enable professional PDF and Excel report exports for institutional analysis.",
        "<b>Scalable Architecture:</b> Build modular, maintainable code that can be extended for multi-institution deployment.",
    ]
    for o in objs: e.append(bullet(o))
    
    e.append(h1("3. SCOPE OF THE PROJECT"))
    scopes = [
        "Design and development of a web-based dropout prediction system for higher education institutions.",
        "Real-time risk assessment using ML with actionable counselling recommendations.",
        "MySQL database integration with support for Admin, Counsellor, and Student roles.",
        "Complete lifecycle coverage from dataset generation and model training to web deployment.",
        "End-to-end system for colleges to monitor student performance and reduce dropout rates.",
    ]
    for s in scopes: e.append(bullet(s))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 4. LITERATURE SURVEY + EXISTING SYSTEM
    # ════════════════════════════════════════════════════════
    e.append(h1("4. LITERATURE SURVEY"))
    e.append(body("A comprehensive review of existing research in student dropout prediction was conducted:"))
    lit_rows = [
        ["1", "X. Chen et al. (2022)", "Student Dropout Prediction Review", "Ensemble methods (RF, GB) achieve highest accuracy"],
        ["2", "M. Kumar & R. Singh (2021)", "Deep Learning for Performance", "DNN achieves 91% accuracy; CGPA, attendance top predictors"],
        ["3", "S. Patel & A. Joshi (2023)", "Web Counselling Platform", "Flask-based platform; automated recommendations effective"],
        ["4", "L. Wang et al. (2020)", "EDM for Dropout Prediction", "Decision trees/SVM; 85% accuracy with 15 features"],
        ["5", "R. Sharma (2023)", "Gradient Boosting for Imbalanced Data", "F1-score of 0.89 on imbalanced dropout datasets"],
        ["6", "K. Yamamoto (2021)", "Feature Engineering for Risk", "Study hours, parent education, internet access critical"],
    ]
    e.append(make_table(["S.No", "Author(s) & Year", "Title", "Key Findings"], lit_rows, col_widths=[0.9*cm, 3.3*cm, 3.8*cm, 7*cm]))
    e.append(sp(4))
    e.append(body("Gradient Boosting consistently outperforms other algorithms. Key predictive features include CGPA, attendance, backlog count, family income, and parent education level."))
    
    e.append(h1("5. EXISTING SYSTEM"))
    exist = [
        "<b>Manual Monitoring:</b> Performance tracked via spreadsheets; no real-time identification of at-risk students.",
        "<b>Reactive Approach:</b> Interventions occur after academic decline, not proactively before dropout.",
        "<b>No ML Integration:</b> Systems lack predictive capability for future dropout risk assessment.",
        "<b>Limited Access:</b> Desktop-based systems restrict usage to specific campus locations.",
        "<b>Generic Counselling:</b> Recommendations are manual and not data-driven, reducing effectiveness.",
        "<b>No Role-Based Access:</b> Single view for all users causes information overload.",
        "<b>No Automated Reports:</b> Manual report generation is time-consuming and error-prone.",
    ]
    for ex in exist: e.append(bullet(ex))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 5. PROPOSED SYSTEM + ARCHITECTURE
    # ════════════════════════════════════════════════════════
    e.append(h1("6. PROPOSED SYSTEM"))
    e.append(body("The proposed system addresses limitations of existing systems with the following features:"))
    feats = [
        "<b>AI-Powered Prediction:</b> Gradient Boosting Classifier with 98.80% accuracy using 8 input features.",
        "<b>Real-Time Assessment:</b> Live predictions whenever academic data is updated, ensuring current risk status.",
        "<b>Automated Recommendations:</b> Context-aware counselling based on risk level and specific academic factors.",
        "<b>Three-Role Architecture:</b> Dedicated dashboards for Admin, Counsellor, and Student with tailored views.",
        "<b>Centralized Management:</b> Student profiles, academics, behaviour, and counselling in one system.",
        "<b>Report Generation:</b> One-click PDF and Excel report exports with professional formatting.",
        "<b>Notification System:</b> In-app alerts for updates, risk assessments, and follow-up reminders.",
        "<b>Secure Authentication:</b> bcrypt hashing, CSRF protection, session management, account lockout.",
    ]
    for f in feats: e.append(bullet(f))
    e.append(sp(4))
    e.append(tbl_cap(1, "Comparison: Existing vs Proposed System"))
    comp_rows = [
        ["Manual tracking", "Automated AI-powered tracking"],
        ["Reactive intervention", "Predictive early warning system"],
        ["No ML integration", "Gradient Boosting engine"],
        ["Desktop-only access", "Web-based (anywhere access)"],
        ["Generic counselling", "Personalized AI recommendations"],
        ["Single user view", "Role-based dashboards"],
        ["Manual reports", "Auto-generated PDF/Excel"],
    ]
    e.append(make_table(["Existing System", "Proposed System"], comp_rows, col_widths=[6.5*cm, 9*cm]))
    
    e.append(h1("7. SYSTEM ARCHITECTURE"))
    e.append(body("The system follows a four-tier architecture ensuring scalability, maintainability, and security:"))
    e.append(ArchitectureDiagram())
    e.extend(fig_cap(1, "System Architecture Diagram", "Four-layer architecture with Presentation, Application, ML, and Data layers"))
    e.append(sp(2))
    e.append(bullet("<b>Presentation Layer:</b> Jinja2 HTML templates with Bootstrap 5, custom CSS, and role-specific dashboards."))
    e.append(bullet("<b>Application Layer:</b> Flask routes with blueprint-based modular organization and service classes for business logic."))
    e.append(bullet("<b>ML Layer:</b> Scikit-learn pipeline (StandardScaler + GradientBoostingClassifier) loaded via singleton pattern for performance."))
    e.append(bullet("<b>Data Layer:</b> MySQL with 9 normalized tables and centralized connectivity via db_helper module."))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 6. DATABASE DESIGN + TECHNOLOGY STACK
    # ════════════════════════════════════════════════════════
    e.append(h1("8. DATABASE DESIGN"))
    e.append(body("The MySQL database uses a normalized schema with 9 tables, foreign key constraints, and strategic indexing for performance optimization."))
    db_rows = [
        ["users", "User accounts (Admin, Student, Counsellor)", "user_id (PK)"],
        ["students", "Student profiles linked to users", "student_id (PK), user_id (FK)"],
        ["academic_records", "Semester-wise CGPA, attendance, marks", "academic_id (PK), student_id (FK)"],
        ["behaviour_records", "Behavioural & socio-economic data", "behaviour_id (PK), student_id (FK)"],
        ["dropout_predictions", "AI prediction results with risk level", "prediction_id (PK), student_id (FK)"],
        ["counselling_recommendations", "Counselling notes and follow-ups", "recommendation_id (PK)"],
        ["notifications", "In-app notification system", "notif_id (PK), user_id (FK)"],
        ["login_history", "Login audit trail", "login_id (PK), user_id (FK)"],
        ["system_logs", "Application activity logs", "log_id (PK)"],
    ]
    e.append(make_table(["Table Name", "Description", "Primary Key(s)"], db_rows, col_widths=[3*cm, 7.5*cm, 5*cm]))
    e.append(sp(4))
    e.append(body_b("Entity-Relationship Diagram:"))
    e.append(ERDiagram())
    e.extend(fig_cap(2, "Entity-Relationship Diagram", "Normalized schema showing tables, attributes, and foreign key relationships"))
    
    e.append(h1("9. TECHNOLOGY STACK"))
    tech_rows = [
        ["Flask 3.1.1", "Python Web Framework", "Routing, session management, template rendering"],
        ["Python 3.x", "Language", "Application logic, ML integration, data processing"],
        ["MySQL", "Database", "Persistent storage with FK constraints and indexes"],
        ["Scikit-Learn 1.7.1", "ML Library", "Gradient Boosting, StandardScaler, pipeline"],
        ["Pandas 2.3.1", "Data Processing", "Data loading, feature extraction, analysis"],
        ["NumPy 2.2.6", "Computing", "Array operations, mathematical computations"],
        ["Jinja2 3.1.6", "Templating", "Server-side HTML rendering with inheritance"],
        ["Bootstrap 5", "CSS Framework", "Responsive UI components and grid system"],
        ["ReportLab 4.4.2", "PDF Generation", "Professional PDF report creation"],
        ["OpenPyXL 3.1.5", "Excel Export", "Formatted Excel report generation"],
        ["BCrypt 4.3.0", "Security", "Password hashing and verification"],
        ["Joblib 1.5.1", "ML Serialization", "Model pipeline save/load"],
        ["Flask-Login", "Auth", "User authentication and session handling"],
        ["Flask-WTF", "Security", "CSRF protection and form validation"],
    ]
    e.append(make_table(["Technology", "Type", "Purpose"], tech_rows, col_widths=[3.5*cm, 3*cm, 9*cm]))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 7. MODULE DESCRIPTION
    # ════════════════════════════════════════════════════════
    e.append(h1("10. MODULE DESCRIPTION"))
    
    e.append(h2("10.1 Authentication Module"))
    e.append(body("Handles registration, login, logout, and session management with role-based access (Admin, Counsellor, Student). Implements bcrypt hashing, failed attempt tracking, and 60-second account lockout."))
    e.append(bullet("Role-based registration with email uniqueness and password strength validation"))
    e.append(bullet("Secure login with bcrypt hashing, failed attempt tracking (5 attempts = lockout)"))
    e.append(bullet("CSRF protection and Flask-Login session management"))
    e.append(bullet("Role-based redirect to respective dashboards after login"))
    
    e.append(h2("10.2 Student Module"))
    e.append(body("Personalized dashboard for academic records, prediction results, and recommendations. Implemented in <b>student_routes.py</b> and <b>academic_service.py</b>."))
    e.append(bullet("Dashboard with latest prediction, risk indicator, and academic overview"))
    e.append(bullet("Semester-wise academic CRUD (CGPA, attendance, internal marks, backlogs)"))
    e.append(bullet("Prediction history tracking and profile management"))
    
    e.append(h2("10.3 Admin Module"))
    e.append(body("System administration dashboard with user/student management and analytics. Implemented in <b>admin_routes.py</b>."))
    e.append(bullet("Statistics dashboard (students, counsellors, predictions, risk distribution)"))
    e.append(bullet("Student and counsellor management with activate/deactivate controls"))
    e.append(bullet("PDF and Excel report generation and data export"))
    
    e.append(h2("10.4 Counsellor Module"))
    e.append(body("Student monitoring and counselling session management. Implemented in <b>counsellor_routes.py</b>."))
    e.append(bullet("Risk-ranked student list with High/Medium/Low filters"))
    e.append(bullet("Counselling notes with follow-up scheduling and status tracking"))
    e.append(bullet("Student detail view with AI prediction and academic summary"))
    
    e.append(h2("10.5 AI Prediction Module"))
    e.append(body("Core ML engine using Gradient Boosting with 8 features. Implemented in <b>prediction_service.py</b> and <b>ml_model_service.py</b>."))
    e.append(bullet("Scikit-learn pipeline with StandardScaler + GradientBoostingClassifier"))
    e.append(bullet("Post-processing logic adjusting probabilities based on academic thresholds"))
    e.append(bullet("Singleton model loading and graceful fallback mechanism"))
    
    e.append(h2("10.6 Reports & Notification Modules"))
    e.append(body("Report module generates PDF/Excel exports via <b>report_service.py</b> and <b>pdf_service.py</b>. Notification module manages in-app alerts via <b>notification_service.py</b>."))
    e.append(bullet("Dashboard stats aggregation and professional PDF generation (ReportLab)"))
    e.append(bullet("Excel export with formatted data (OpenPyXL)"))
    e.append(bullet("User-specific notifications with read/unread tracking"))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 8. AI MODEL WORKING
    # ════════════════════════════════════════════════════════
    e.append(h1("11. AI MODEL WORKING"))
    
    e.append(h2("11.1 Dataset"))
    e.append(body("Synthetic dataset of <b>2,000 student records</b> with 8 features and binary target (dropout). Generated using realistic risk scoring in <b>generate_dataset.py</b> where risk score >= 7 labels dropout=1."))
    
    feat_rows = [
        ["cgpa",  "0-10", "Cumulative GPA", "Lower = higher risk"],
        ["attendance", "0-100%", "Class attendance", "<65% = critical"],
        ["internal_marks", "0-100", "Internal assessment", "Consistent effort"],
        ["backlog_count", "0+", "Pending backlogs", ">4 = high risk"],
        ["study_hours", "0-24", "Daily study hours", "<2 hrs = risk"],
        ["family_income", "INR", "Annual income", "Socio-economic factor"],
        ["parent_education", "0-3", "Education level", "Parental influence"],
        ["internet_access", "0/1", "Internet at home", "Digital divide"],
    ]
    e.append(make_table(["Feature", "Type", "Description", "Impact"], feat_rows, col_widths=[2.5*cm, 2*cm, 4*cm, 4.5*cm]))
    
    e.append(h2("11.2 Model Training Pipeline"))
    e.append(body("Training pipeline implemented in <b>train_model.py</b>:"))
    e.append(bullet("80-20 train-test split with stratification to maintain class distribution"))
    e.append(bullet("StandardScaler normalization followed by GradientBoostingClassifier"))
    e.append(bullet("Hyperparameters: 200 estimators, learning rate 0.05, max depth 4"))
    e.append(bullet("<b>Accuracy: 98.80%</b> | Precision: 0.99 | Recall: 0.98 for dropout class"))
    e.append(bullet("Pipeline serialized via joblib for production deployment"))
    
    # Prediction flow
    flow_lines = [
        "Student Data (DB) -----> 8 Features Extracted -----> ML Pipeline",
        "                              |                           |",
        "                              v                           v",
        "                     Post-Processing <--- Probability & Risk Level",
        "                              |",
        "                              v",
        "                     Recommendation Generation"
    ]
    fl = "<br/>".join(flow_lines)
    e.append(Paragraph(fl, ParagraphStyle('FLW', fontName='Courier', fontSize=8, leading=12, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4, backColor=LIGHT_BLUE, borderColor=BORDER_CLR, borderWidth=0.5, borderPadding=6)))
    e.extend(fig_cap(3, "AI Model Prediction Flow", "End-to-end flow from data extraction to recommendation generation"))
    
    e.append(h2("11.3 Risk Levels"))
    risk_rows = [
        ["Low", "< 35%", "Green", "Maintain current habits"],
        ["Medium", "35-60%", "Amber", "Monitor and support required"],
        ["High", ">= 60%", "Red", "Immediate intervention needed"],
    ]
    e.append(make_table(["Risk Level", "Probability", "Indicator", "Action"], risk_rows, col_widths=[2.5*cm, 3*cm, 2.5*cm, 5.5*cm]))
    
    e.append(h2("11.4 Recommendation Generation"))
    e.append(body("The <b>recommendation_service.py</b> generates context-aware recommendations:"))
    e.append(bullet("<b>High Risk:</b> 'Immediate counselling required. Low attendance (45.2%), 5 pending backlogs. Faculty mentoring essential.'"))
    e.append(bullet("<b>Medium Risk:</b> 'Performance needs improvement. Attendance below 75%. Increase study hours, join peer groups.'"))
    e.append(bullet("<b>Low Risk:</b> 'Excellent performance! Maintain CGPA 8.5+, continue current study habits.'"))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 9. SOFTWARE CODING DEMONSTRATION
    # ════════════════════════════════════════════════════════
    e.append(h1("12. SOFTWARE CODING DEMONSTRATION"))
    e.append(body("Key code snippets from the actual project source:"))
    
    e.append(h2("12.1 Flask Application Factory"))
    e.append(code("def create_app():<br/>    app = Flask(__name__)<br/>    app.config.from_object(Config)<br/>    init_extensions(app)<br/>    app.register_blueprint(auth_bp)<br/>    app.register_blueprint(student_bp)<br/>    app.register_blueprint(admin_bp)<br/>    app.register_blueprint(counsellor_bp)<br/>    app.register_blueprint(api_bp)<br/>    register_error_handlers(app)<br/>    return app"))
    
    e.append(h2("12.2 ML Training Pipeline"))
    e.append(code("pipeline = Pipeline([<br/>    ('scaler', StandardScaler()),<br/>    ('model', GradientBoostingClassifier(<br/>        n_estimators=200, learning_rate=0.05,<br/>        max_depth=4, random_state=42<br/>    ))<br/>])<br/>pipeline.fit(X_train, y_train)<br/>print(f'Accuracy: {accuracy_score(y_test, pipeline.predict(X_test))*100:.2f}%')"))
    
    e.append(h2("12.3 Prediction Service"))
    e.append(code("class dropout_predictionservice:<br/>    @staticmethod<br/>    def predict_dropout(student_id):<br/>        data = AcademicModel.get_student_academic_summary(student_id)<br/>        features = {<br/>            'cgpa': data['cgpa'], 'attendance': data['attendance'],<br/>            'backlog_count': data['backlog_count'], 'study_hours': data['study_hours'],<br/>            'family_income': 50000, 'parent_education': 2, 'internet_access': 1<br/>        }<br/>        result = MLModelService.predict(features)<br/>        return {'risk_level': result['risk_level'], 'probability': result['probability']}"))
    
    e.append(h2("12.4 Post-Processing Logic"))
    e.append(code("if cgpa >= 8.0 and attendance >= 85 and backlog_count == 0:<br/>    risk_level = 'Low'   # Excellent student<br/>elif cgpa < 5.5 or attendance < 55 or backlog_count >= 4:<br/>    risk_level = 'High'  # Critical indicators<br/>elif cgpa < 6.5 or attendance < 65 or backlog_count >= 2:<br/>    risk_level = 'Medium'<br/>else:<br/>    risk_level = 'Low' if adjusted_prob < 35 else 'Medium'"))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 10. OUTPUT SCREENSHOTS
    # ════════════════════════════════════════════════════════
    e.append(h1("13. OUTPUT SCREENSHOTS"))
    e.append(body("The following screenshots from the running application demonstrate key features:"))
    
    screens = [
        ("4", "Login Page", "Secure authentication interface"),
        ("5", "Registration Page", "User registration with role selection"),
        ("6", "Student Dashboard", "Risk indicator and academic overview"),
        ("7", "Academic Record Form", "Semester data entry (CGPA, attendance)"),
        ("8", "Prediction Result", "Risk level with recommendation"),
        ("9", "Admin Dashboard", "System statistics and analytics"),
        ("10", "Student Management", "Admin student list with details"),
        ("11", "Counsellor Dashboard", "Risk-monitoring interface"),
        ("12", "At-Risk Students", "High/Medium risk filtered view"),
        ("13", "Counselling Notes", "Session tracking with status"),
        ("14", "Reports Page", "Analytics with export options"),
        ("15", "Confusion Matrix", "Model performance visualization"),
    ]
    for num, title, desc in screens:
        e.append(Paragraph(f"<b>Figure {num}: {title}</b> — {desc}", ParagraphStyle('SC', fontName='Times-Roman', fontSize=11, leading=16, textColor=DARK_TEXT, spaceBefore=3, spaceAfter=1)))
    e.append(sp(8))
    e.append(body("All screenshots are attached from the existing <b>output_report/screenshots.pdf</b> file."))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 11. FUTURE WORK + CONCLUSION
    # ════════════════════════════════════════════════════════
    e.append(h1("14. FUTURE WORK"))
    futures = [
        "<b>Deep Learning:</b> LSTM/Transformer models for sequential semester analysis.",
        "<b>LMS Integration:</b> Real-time sync with institutional Learning Management Systems.",
        "<b>Mobile App:</b> Cross-platform app (React Native/Flutter) for on-the-go access.",
        "<b>Advanced Analytics:</b> Interactive dashboards with Chart.js/D3.js visualizations.",
        "<b>Multi-Institution:</b> Tenant-based data isolation for multiple college support.",
        "<b>SMS/Email Alerts:</b> Twilio/SendGrid integration for automated outreach.",
        "<b>Explainable AI:</b> SHAP/LIME for model interpretability and trust.",
        "<b>Parent Portal:</b> Guardian access for monitoring student progress.",
    ]
    for f in futures: e.append(bullet(f))
    
    e.append(h1("15. CONCLUSION"))
    e.append(body("The AI-Based Student Dropout Prediction and Counselling System successfully demonstrates the practical application of machine learning to address student dropout in higher education. The Gradient Boosting model achieves <b>98.80% accuracy</b> using 8 features, categorizing students into Low, Medium, and High risk categories."))
    e.append(body("The web application provides role-specific dashboards for Administrators, Counsellors, and Students, with features including real-time prediction, automated recommendations, PDF/Excel reports, and notification services. The modular architecture ensures scalability and maintainability."))
    e.append(body("By identifying at-risk students early and providing data-driven counselling recommendations, the system empowers educational institutions to take proactive measures in reducing dropout rates and improving student outcomes."))
    e.append(new_page())

    # ════════════════════════════════════════════════════════
    # 12. REFERENCES
    # ════════════════════════════════════════════════════════
    e.append(h1("16. REFERENCES"))
    refs = [
        "1. Chen, X., Wang, Y., & Liu, Z. (2022). 'Student Dropout Prediction Using Machine Learning: A Review.' IEEE Trans. on Learning Technologies, 15(3), 456-470.",
        "2. Kumar, M., & Singh, R. (2021). 'Deep Learning for Student Performance Prediction.' Int. J. of AI in Education, 31(2), 234-251.",
        "3. Patel, S., & Joshi, A. (2023). 'Web-Based Counselling Platform for At-Risk Students.' J. of Educational Technology Systems, 51(4), 389-405.",
        "4. Wang, L., Zhang, Y., & Chen, H. (2020). 'EDM for Dropout Prediction: A Comparative Study.' Computers & Education, 145, 103-118.",
        "5. Sharma, R. (2023). 'Gradient Boosting for Imbalanced Educational Datasets.' Machine Learning with Applications, 12, 100-115.",
        "6. Yamamoto, K. (2021). 'Feature Engineering for Academic Risk Assessment.' Educational Technology Research, 69(5), 1123-1140.",
        "7. Pedregosa, F. et al. (2011). 'Scikit-learn: Machine Learning in Python.' JMLR, 12, 2825-2830.",
        "8. Grinberg, M. (2018). Flask Web Development, 2nd Ed. O'Reilly Media.",
        "9. Geron, A. (2022). Hands-On Machine Learning with Scikit-Learn, 3rd Ed. O'Reilly.",
        "10. MySQL 8.0 Reference Manual. Oracle. https://dev.mysql.com/doc/",
        "11. Bootstrap 5 Documentation. https://getbootstrap.com/docs/5.0/",
        "12. Flask 3.1 Documentation. https://flask.palletsprojects.com/",
    ]
    for r in refs: e.append(Paragraph(r, ref_style))

    # ════════════════════════════════════════════════════════
    # BUILD
    # ════════════════════════════════════════════════════════
    doc.build(e, onFirstPage=set_hf, onLaterPages=set_hf)
    buf.seek(0)
    return buf

def merge_screenshots(report_buf, screenshot_path, output_path):
    try:
        r = PdfReader(report_buf)
        s = PdfReader(screenshot_path)
        w = PdfWriter()
        for p in r.pages: w.add_page(p)
        for p in s.pages: w.add_page(p)
        with open(output_path, "wb") as f: w.write(f)
        print(f"  Report: {len(r.pages)} pages | Screenshots: {len(s.pages)} pages | Total: {len(r.pages)+len(s.pages)}")
        return True
    except Exception as ex:
        print(f"  Merge failed: {ex}")
        return False

if __name__ == "__main__":
    print("=" * 55)
    print("  AI-Based Student Dropout Prediction & Counselling")
    print("  Final Year Project Report Generator (v2)")
    print("=" * 55)
    print()
    print("Generating report...")
    buf = build_report()
    print("  Report generated successfully.")
    print()
    if os.path.exists(SCREENSHOT_PDF):
        print(f"Merging screenshots: {SCREENSHOT_PDF}")
        ok = merge_screenshots(buf, SCREENSHOT_PDF, OUTPUT_PDF)
        if not ok:
            with open(OUTPUT_PDF, "wb") as f: f.write(buf.getvalue())
            print("  Saved without screenshots.")
    else:
        with open(OUTPUT_PDF, "wb") as f: f.write(buf.getvalue())
        print(f"  No screenshots found. Saved report only.")
    print(f"\n  Output: {OUTPUT_PDF}")
    print("=" * 55)