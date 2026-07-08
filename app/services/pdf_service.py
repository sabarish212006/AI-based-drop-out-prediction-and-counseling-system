"""
----------------------------------------------------------
AI-Based Student Dropout Prediction and Counselling System
File: pdf_service.py
Purpose: Generate Professional PDF Reports (System & Student)
----------------------------------------------------------
"""

import io
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Headless mode
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image as RLImage,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class PDFService:
    """
    Service to generate professional, presentation-ready PDF reports.
    """

    @staticmethod
    def _create_header_footer(canvas, doc):
        """
        Draws professional header and footer accents on pages.
        """
        canvas.saveState()
        # Top primary color bar (Navy Blue)
        canvas.setFillColor(colors.HexColor("#0f172a"))
        canvas.rect(0, doc.pagesize[1] - 15, doc.pagesize[0], 15, stroke=0, fill=1)
        
        # Bottom secondary color accent
        canvas.setFillColor(colors.HexColor("#3b82f6"))
        canvas.rect(0, 0, doc.pagesize[0], 10, stroke=0, fill=1)
        
        # Footer text
        canvas.setFont("Helvetica-Oblique", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(54, 25, "Confidential - AI-Based Dropout Prediction & Counselling System")
        canvas.drawRightString(doc.pagesize[0] - 54, 25, f"Page {doc.page} | Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
        canvas.restoreState()

    @staticmethod
    def generate_system_report(stats):
        """
        Generates system-wide analytics report with charts and tables.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0f172a'),
            alignment=0, # Left aligned
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'DocSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=20
        )
        
        h1_style = ParagraphStyle(
            'H1',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1e3a8a'),
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True
        )

        cell_style = ParagraphStyle(
            'CellText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#334155')
        )
        
        cell_bold_style = ParagraphStyle(
            'CellTextBold',
            parent=cell_style,
            fontName='Helvetica-Bold'
        )

        elements = []

        # =====================================
        # TITLE BLOCK
        # =====================================
        elements.append(Paragraph("AI-Based Dropout Prediction & Counselling System", title_style))
        elements.append(Paragraph(f"<b>System Analytics & Health Report</b> &nbsp;|&nbsp; Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
        elements.append(Spacer(1, 10))

        # =====================================
        # 1. METRICS OVERVIEW TABLE
        # =====================================
        elements.append(Paragraph("System Statistics Overview", h1_style))
        
        metrics_data = [
            [Paragraph("<b>Metric</b>", cell_bold_style), Paragraph("<b>Value</b>", cell_bold_style), Paragraph("<b>Context / Details</b>", cell_bold_style)],
            [Paragraph("Total Students", cell_style), Paragraph(str(stats.get("total_students", 0)), cell_bold_style), Paragraph("Registered student accounts in system", cell_style)],
            [Paragraph("Total Counsellors", cell_style), Paragraph(str(stats.get("total_counsellors", 0)), cell_bold_style), Paragraph("Active counsellors in mentoring panels", cell_style)],
            [Paragraph("Total Predictions", cell_style), Paragraph(str(stats.get("total_predictions", 0)), cell_bold_style), Paragraph("Saved AI prediction histories", cell_style)],
            [Paragraph("High Risk Students", cell_style), Paragraph(str(stats.get("high_risk_students", 0)), cell_bold_style), Paragraph("Require immediate counselling attention", cell_style)],
            [Paragraph("Medium Risk Students", cell_style), Paragraph(str(stats.get("medium_risk_students", 0)), cell_bold_style), Paragraph("Needs monitoring and timely follow-ups", cell_style)],
            [Paragraph("Low Risk Students", cell_style), Paragraph(str(stats.get("low_risk_students", 0)), cell_bold_style), Paragraph("Satisfactory performance indicators", cell_style)],
        ]
        
        t1 = Table(metrics_data, colWidths=[150, 80, 274])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#cbd5e1')),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(t1)
        elements.append(Spacer(1, 15))

        # =====================================
        # 2. ACADEMIC HEALTH SUMMARY TABLE
        # =====================================
        elements.append(Paragraph("Academic Health Metrics", h1_style))
        academic = stats.get("academic_summary", {})
        
        academic_data = [
            [Paragraph("<b>Performance Indicator</b>", cell_bold_style), Paragraph("<b>Average Value</b>", cell_bold_style)],
            [Paragraph("Average CGPA", cell_style), Paragraph(str(academic.get("average_cgpa", "N/A")), cell_bold_style)],
            [Paragraph("Average Attendance", cell_style), Paragraph(f"{academic.get('average_attendance', 'N/A')} %", cell_bold_style)],
            [Paragraph("Total Academic Records Checked", cell_style), Paragraph(str(academic.get("total_records", "N/A")), cell_bold_style)]
        ]
        t2 = Table(academic_data, colWidths=[280, 224])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#cbd5e1')),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(t2)
        elements.append(Spacer(1, 20))

        # =====================================
        # 3. GRAPHICAL VISUALIZATIONS (Matplotlib)
        # =====================================
        elements.append(Paragraph("System Graphical Insights", h1_style))
        
        # Build Pie Chart
        fig, ax = plt.subplots(figsize=(6, 3))
        labels = ['High Risk', 'Medium Risk', 'Low Risk']
        sizes = [stats.get('high_risk_students', 0), stats.get('medium_risk_students', 0), stats.get('low_risk_students', 0)]
        colors_list = ['#ef4444', '#f59e0b', '#10b981'] # tailwind red, amber, emerald
        
        if sum(sizes) == 0:
            sizes = [1, 1, 1]
            labels = ['No Data', 'No Data', 'No Data']
            colors_list = ['#cbd5e1', '#cbd5e1', '#cbd5e1']
            
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_list, startangle=90, textprops={'fontsize': 9})
        ax.axis('equal')
        plt.title('Student Risk Distribution', fontsize=11, fontweight='bold', pad=5)
        plt.tight_layout()
        
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', dpi=150)
        plt.close(fig)
        img_buf.seek(0)
        
        chart_flowable = RLImage(img_buf, width=4.5 * inch, height=2.25 * inch)
        elements.append(KeepTogether([chart_flowable]))
        
        doc.build(elements, onFirstPage=PDFService._create_header_footer, onLaterPages=PDFService._create_header_footer)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_student_report(student, academic, prediction, academic_history, counselling_notes):
        """
        Generates individual student report suitable for presentation or print.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0f172a'),
            alignment=0,
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'DocSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15
        )
        
        h1_style = ParagraphStyle(
            'H1',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        )

        cell_style = ParagraphStyle(
            'CellText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#334155')
        )
        
        cell_bold_style = ParagraphStyle(
            'CellTextBold',
            parent=cell_style,
            fontName='Helvetica-Bold'
        )

        elements = []

        # =====================================
        # TITLE BLOCK
        # =====================================
        elements.append(Paragraph("AI Dropout Prediction - Student Case File", title_style))
        elements.append(Paragraph(f"<b>Roll No:</b> {student.get('roll_no', 'N/A')} &nbsp;|&nbsp; <b>Name:</b> {student.get('full_name', 'N/A')} &nbsp;|&nbsp; <b>Generated:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}", subtitle_style))
        elements.append(Spacer(1, 5))

        # =====================================
        # 1. PROFILE DETAILS TABLE
        # =====================================
        elements.append(Paragraph("Student Profile Information", h1_style))
        profile_data = [
            [Paragraph("<b>Full Name</b>", cell_bold_style), Paragraph(student.get("full_name", "N/A"), cell_style),
             Paragraph("<b>Roll Number</b>", cell_bold_style), Paragraph(student.get("roll_no", "N/A"), cell_style)],
            [Paragraph("<b>Department</b>", cell_bold_style), Paragraph(student.get("department", "N/A"), cell_style),
             Paragraph("<b>Year of Study</b>", cell_bold_style), Paragraph(f"Year {student.get('year_of_study', 'N/A')}", cell_style)],
            [Paragraph("<b>Email ID</b>", cell_bold_style), Paragraph(student.get("email", "N/A"), cell_style),
             Paragraph("<b>Phone / Contact</b>", cell_bold_style), Paragraph(student.get("phone") or "N/A", cell_style)],
            [Paragraph("<b>Gender</b>", cell_bold_style), Paragraph(student.get("gender") or "N/A", cell_style),
             Paragraph("<b>Date of Birth</b>", cell_bold_style), Paragraph(str(student.get("date_of_birth") or "N/A"), cell_style)],
            [Paragraph("<b>Address</b>", cell_bold_style), Paragraph(student.get("address") or "N/A", cell_style),
             Paragraph("", cell_bold_style), Paragraph("", cell_style)]
        ]
        t1 = Table(profile_data, colWidths=[100, 150, 100, 154])
        t1.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('SPAN', (1, 4), (3, 4)), # merge address columns
        ]))
        elements.append(t1)
        elements.append(Spacer(1, 10))

        # =====================================
        # 2. AI PREDICTION SUMMARY
        # =====================================
        elements.append(Paragraph("AI Dropout Prediction & Risk Assessment", h1_style))
        risk_level = prediction.get("risk_level", "Low")
        
        # Color code the badge style
        badge_bg = "#10b981" # Green
        badge_text = "#ffffff"
        if risk_level == "High":
            badge_bg = "#ef4444" # Red
        elif risk_level == "Medium":
            badge_bg = "#f59e0b" # Yellow
            badge_text = "#1e293b"

        prob = prediction.get("probability") or prediction.get("score") or 0.0
        
        risk_badge_style = ParagraphStyle(
            'RiskBadge',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor(badge_text),
            backColor=colors.HexColor(badge_bg),
            borderPadding=4,
            spaceAfter=0,
            alignment=1 # Center aligned
        )

        prediction_data = [
            [Paragraph("<b>Risk Classification</b>", cell_bold_style), Paragraph(f"<b>{risk_level.upper()} RISK</b>", risk_badge_style),
             Paragraph("<b>Dropout Probability</b>", cell_bold_style), Paragraph(f"{prob:.2f} %", cell_bold_style)],
            [Paragraph("<b>Model Version</b>", cell_bold_style), Paragraph(prediction.get("model_version", "v1"), cell_style),
             Paragraph("<b>Last Prediction Run</b>", cell_bold_style), Paragraph(prediction.get("prediction_date") or prediction.get("predicted_on") or "N/A", cell_style)],
            [Paragraph("<b>AI Narrative / Recommendation</b>", cell_bold_style), Paragraph(prediction.get("recommendation") or prediction.get("explanation") or "N/A", cell_style),
             Paragraph("", cell_bold_style), Paragraph("", cell_style)]
        ]
        
        t2 = Table(prediction_data, colWidths=[130, 120, 120, 134])
        t2.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('SPAN', (1, 2), (3, 2)), # merge recommendation
        ]))
        elements.append(t2)
        elements.append(Spacer(1, 10))

        # =====================================
        # 3. TRENDS / CHARTS
        # =====================================
        if academic_history:
            elements.append(Paragraph("Academic CGPA & Attendance Performance Trends", h1_style))
            
            # Sort by semester
            records = sorted(academic_history, key=lambda x: x.get('semester', 0))
            semesters = [f"Sem {r.get('semester')}" for r in records]
            cgpas = [float(r.get('cgpa', 0)) for r in records]
            attendances = [float(r.get('attendance', 0)) for r in records]
            
            fig, ax1 = plt.subplots(figsize=(6, 2.2))
            
            color = '#3b82f6' # tailwind blue
            ax1.set_xlabel('Semester', fontweight='bold', fontsize=8)
            ax1.set_ylabel('CGPA', color=color, fontweight='bold', fontsize=8)
            ax1.plot(semesters, cgpas, color=color, marker='o', linewidth=2, label='CGPA')
            ax1.tick_params(axis='y', labelcolor=color, labelsize=8)
            ax1.tick_params(axis='x', labelsize=8)
            ax1.set_ylim(0, 10.5)
            
            ax2 = ax1.twinx()  
            color = '#10b981' # tailwind emerald
            ax2.set_ylabel('Attendance (%)', color=color, fontweight='bold', fontsize=8)
            ax2.bar(semesters, attendances, color=color, alpha=0.25, width=0.35, label='Attendance')
            ax2.tick_params(axis='y', labelcolor=color, labelsize=8)
            ax2.set_ylim(0, 110)
            
            plt.title('Semester-wise Academic Metrics', fontsize=10, fontweight='bold')
            fig.tight_layout()
            
            trend_buf = io.BytesIO()
            plt.savefig(trend_buf, format='png', dpi=150)
            plt.close(fig)
            trend_buf.seek(0)
            
            trend_flowable = RLImage(trend_buf, width=4.8 * inch, height=1.76 * inch)
            elements.append(KeepTogether([trend_flowable]))
            elements.append(Spacer(1, 10))

        # =====================================
        # 4. ACADEMIC RECORDS HISTORY
        # =====================================
        elements.append(Paragraph("Detailed Academic History", h1_style))
        hist_table = [
            [Paragraph("<b>Sem</b>", cell_bold_style), Paragraph("<b>CGPA</b>", cell_bold_style), Paragraph("<b>Attendance</b>", cell_bold_style), Paragraph("<b>Internal Marks</b>", cell_bold_style), Paragraph("<b>Backlogs</b>", cell_bold_style), Paragraph("<b>Study Hrs</b>", cell_bold_style)]
        ]
        
        for r in academic_history:
            hist_table.append([
                Paragraph(str(r.get("semester")), cell_style),
                Paragraph(f"{float(r.get('cgpa', 0)):.2f}", cell_style),
                Paragraph(f"{float(r.get('attendance', 0)):.1f}%", cell_style),
                Paragraph(f"{float(r.get('internal_marks', 0)):.1f}", cell_style),
                Paragraph(str(r.get("backlog_count", 0)), cell_style),
                Paragraph(f"{float(r.get('study_hours', 0)):.1f} hrs", cell_style)
            ])
            
        t3 = Table(hist_table, colWidths=[50, 80, 94, 94, 94, 92])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#cbd5e1')),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(t3)
        elements.append(Spacer(1, 10))

        # =====================================
        # 5. COUNSELLING TIMELINE NOTES
        # =====================================
        elements.append(Paragraph("Mentoring & Counselling Actions Log", h1_style))
        counselling_table = [
            [Paragraph("<b>Date / Deadline</b>", cell_bold_style), Paragraph("<b>Counsellor</b>", cell_bold_style), Paragraph("<b>Counselling Status</b>", cell_bold_style), Paragraph("<b>Counsellor Recommendation Notes</b>", cell_bold_style)]
        ]
        
        for note in counselling_notes:
            counselling_table.append([
                Paragraph(str(note.get("follow_up_date")), cell_style),
                Paragraph(note.get("counsellor_name") or "N/A", cell_style),
                Paragraph(note.get("status") or "Pending", cell_bold_style),
                Paragraph(note.get("recommendation") or "N/A", cell_style)
            ])
            
        if len(counselling_table) == 1:
            counselling_table.append([Paragraph("No counselling timeline notes logged for this student.", cell_style), Paragraph("", cell_style), Paragraph("", cell_style), Paragraph("", cell_style)])
            
        t4 = Table(counselling_table, colWidths=[90, 110, 84, 220])
        t4.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#cbd5e1')),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        if len(counselling_table) == 2 and counselling_table[1][1] == "":
            t4.setStyle(TableStyle([('SPAN', (0, 1), (3, 1))]))
            
        elements.append(t4)

        doc.build(elements, onFirstPage=PDFService._create_header_footer, onLaterPages=PDFService._create_header_footer)
        buffer.seek(0)
        return buffer