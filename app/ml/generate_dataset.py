"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: generate_dataset.py
Purpose: Generate Synthetic Student Dataset with
         Realistic Dropout Labels
----------------------------------------------------------
Dropout Logic (realistic):
  HIGH risk (dropout=1): CGPA < 5.5 OR attendance < 60% OR backlogs >= 5
  MEDIUM risk: marginal students (labelled 0 with moderate probability)
  LOW risk (dropout=0): Good CGPA, good attendance, low backlogs

A good student (CGPA=7.2, attendance=73.5%, backlogs=0)
MUST predict LOW risk.
----------------------------------------------------------
"""

import os
import random
import pandas as pd

# ==========================================
# CONFIGURATION
# ==========================================

TOTAL_STUDENTS = 2000
random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(RAW_DATA_DIR, "student_dropout.csv")


# ==========================================
# DATASET GENERATION
# ==========================================

dataset = []

for student_id in range(1, TOTAL_STUDENTS + 1):

    # Academic features
    cgpa            = round(random.uniform(4.0, 10.0), 2)
    attendance      = round(random.uniform(40.0, 100.0), 2)
    internal_marks  = round(random.uniform(30.0, 100.0), 2)
    backlog_count   = random.randint(0, 8)
    study_hours     = round(random.uniform(0.5, 8.0), 1)

    # Socio-economic features
    family_income     = random.randint(50000, 500000)
    parent_education  = random.choice([0, 1, 2, 3])   # 0=School,1=Diploma,2=UG,3=PG
    internet_access   = random.choice([0, 1])

    # ======================================
    # REALISTIC DROPOUT LOGIC
    # A student DROPS OUT only if MULTIPLE
    # strong risk factors are present.
    # ======================================

    risk_score = 0

    # Academic risk (most important)
    if cgpa < 5.0:
        risk_score += 4          # Very low CGPA — very high risk
    elif cgpa < 6.0:
        risk_score += 2          # Low CGPA

    if attendance < 55:
        risk_score += 4          # Very poor attendance
    elif attendance < 65:
        risk_score += 2          # Poor attendance
    elif attendance < 75:
        risk_score += 1          # Below average attendance

    if internal_marks < 40:
        risk_score += 3
    elif internal_marks < 50:
        risk_score += 2
    elif internal_marks < 60:
        risk_score += 1

    if backlog_count >= 6:
        risk_score += 4
    elif backlog_count >= 4:
        risk_score += 3
    elif backlog_count >= 2:
        risk_score += 1

    if study_hours < 1.0:
        risk_score += 2
    elif study_hours < 2.0:
        risk_score += 1

    # Socio-economic risk (secondary)
    if family_income < 100000:
        risk_score += 1
    if parent_education == 0:
        risk_score += 1
    if internet_access == 0:
        risk_score += 1

    # Dropout = 1 only if strong evidence (score >= 7)
    # This ensures CGPA=7.2, attendance=73.5%, backlogs=0 → score=1 → dropout=0 (LOW RISK)
    dropout = 1 if risk_score >= 7 else 0

    dataset.append({
        "student_id":       student_id,
        "cgpa":             cgpa,
        "attendance":       attendance,
        "internal_marks":   internal_marks,
        "backlog_count":    backlog_count,
        "study_hours":      study_hours,
        "family_income":    family_income,
        "parent_education": parent_education,
        "internet_access":  internet_access,
        "dropout":          dropout
    })


# ==========================================
# SAVE CSV
# ==========================================

df = pd.DataFrame(dataset)
df.to_csv(OUTPUT_FILE, index=False)

dropout_count = df["dropout"].sum()
print("=" * 55)
print("Dataset Generated Successfully")
print(f"Location      : {OUTPUT_FILE}")
print(f"Total Records : {len(df)}")
print(f"Dropout=1     : {dropout_count} ({dropout_count/len(df)*100:.1f}%)")
print(f"Dropout=0     : {len(df)-dropout_count} ({(len(df)-dropout_count)/len(df)*100:.1f}%)")
print("=" * 55)