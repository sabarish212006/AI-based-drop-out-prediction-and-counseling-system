"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: preprocess.py
Purpose: Data Preprocessing — Encode + Clean + Save
----------------------------------------------------------
"""

import os
import pandas as pd

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA = os.path.join(BASE_DIR, "data", "raw", "student_dropout.csv")

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(PROCESSED_DIR, "processed_dataset.csv")


# ==========================================
# LOAD DATASET
# ==========================================

print("\nLoading dataset...")
df = pd.read_csv(RAW_DATA)
print(f"Records Loaded : {len(df)}")


# ==========================================
# REMOVE DUPLICATES
# ==========================================

duplicates = df.duplicated().sum()
if duplicates > 0:
    df.drop_duplicates(inplace=True)
print(f"Duplicates Removed : {duplicates}")


# ==========================================
# HANDLE MISSING VALUES
# ==========================================

missing = df.isnull().sum().sum()
if missing > 0:
    for column in df.columns:
        if df[column].dtype == "object":
            df[column].fillna(df[column].mode()[0], inplace=True)
        else:
            df[column].fillna(df[column].median(), inplace=True)
print(f"Missing Values Fixed : {missing}")


# ==========================================
# FEATURE ORDER (MUST MATCH prediction_service.py)
# ==========================================
# Features used for prediction:
# cgpa, attendance, internal_marks, backlog_count,
# study_hours, family_income, parent_education, internet_access
# (parent_education is already numeric 0-3 in generate_dataset.py)

FEATURES = [
    "cgpa",
    "attendance",
    "internal_marks",
    "backlog_count",
    "study_hours",
    "family_income",
    "parent_education",
    "internet_access"
]

TARGET = "dropout"

# Verify all features exist
missing_cols = [c for c in FEATURES + [TARGET] if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

# Keep only needed columns (drop student_id)
df_processed = df[FEATURES + [TARGET]].copy()


# ==========================================
# DATA SUMMARY
# ==========================================

print("\nDataset Summary:")
print(df_processed.describe().round(2))

dropout_pct = df_processed[TARGET].mean() * 100
print(f"\nDropout rate: {dropout_pct:.1f}%")


# ==========================================
# SAVE PROCESSED DATASET
# ==========================================

df_processed.to_csv(OUTPUT_FILE, index=False)

print("\n==========================================")
print("Dataset Preprocessing Completed")
print(f"Output        : {OUTPUT_FILE}")
print(f"Final Records : {len(df_processed)}")
print(f"Features      : {FEATURES}")
print("==========================================")