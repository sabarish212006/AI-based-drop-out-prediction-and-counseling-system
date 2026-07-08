"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: train_model.py
Purpose: Train Gradient Boosting Model for Dropout Prediction
----------------------------------------------------------
Feature Order (MUST match prediction_service.py):
  cgpa, attendance, internal_marks, backlog_count,
  study_hours, family_income, parent_education, internet_access
----------------------------------------------------------
"""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR, "data", "processed", "processed_dataset.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "dropout_model.pkl")

# ==========================================
# LOAD DATASET
# ==========================================

print("\nLoading processed dataset...")
df = pd.read_csv(DATASET_PATH)
print(f"Dataset Shape : {df.shape}")

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

X = df[FEATURES]
y = df["dropout"]

print(f"Dropout=1 count : {y.sum()} ({y.mean()*100:.1f}%)")
print(f"Dropout=0 count : {(1-y).sum()} ({(1-y).mean()*100:.1f}%)")

# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"\nTraining Records : {len(X_train)}")
print(f"Testing Records  : {len(X_test)}")

# ==========================================
# PIPELINE: Scaler + Gradient Boosting
# ==========================================

print("\nTraining Gradient Boosting Model...")

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    ))
])

pipeline.fit(X_train, y_train)

# ==========================================
# EVALUATION
# ==========================================

predictions = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("\n========================================")
print(f"Accuracy : {accuracy * 100:.2f}%")
print("========================================\n")
print(classification_report(y_test, predictions))
print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))

# ==========================================
# VALIDATION TEST CASES
# ==========================================

print("\n--- Validation Test Cases ---")
test_cases = [
    {
        "label":          "Good Student (CGPA=7.2, Att=73.5, BL=0)",
        "cgpa":            7.2,
        "attendance":      73.5,
        "internal_marks":  65.0,
        "backlog_count":   0,
        "study_hours":     3.0,
        "family_income":   350000,
        "parent_education": 2,
        "internet_access": 1
    },
    {
        "label":          "Excellent Student (CGPA=9.0, Att=91, BL=0)",
        "cgpa":            9.0,
        "attendance":      91.0,
        "internal_marks":  88.0,
        "backlog_count":   0,
        "study_hours":     5.0,
        "family_income":   500000,
        "parent_education": 3,
        "internet_access": 1
    },
    {
        "label":          "At-Risk Student (CGPA=5.0, Att=55, BL=5)",
        "cgpa":            5.0,
        "attendance":      55.0,
        "internal_marks":  42.0,
        "backlog_count":   5,
        "study_hours":     1.0,
        "family_income":   100000,
        "parent_education": 0,
        "internet_access": 0
    },
    {
        "label":          "Critical Student (CGPA=4.5, Att=48, BL=7)",
        "cgpa":            4.5,
        "attendance":      48.0,
        "internal_marks":  35.0,
        "backlog_count":   7,
        "study_hours":     0.5,
        "family_income":   80000,
        "parent_education": 0,
        "internet_access": 0
    }
]

for tc in test_cases:
    label = tc.pop("label")
    df_tc = pd.DataFrame([tc])
    prob = pipeline.predict_proba(df_tc)[0][1] * 100
    pred = pipeline.predict(df_tc)[0]
    risk = "HIGH" if prob >= 60 else "MEDIUM" if prob >= 35 else "LOW"
    print(f"  {label}")
    print(f"    -> Prediction={pred}, Probability={prob:.1f}%, Risk={risk}")

# ==========================================
# SAVE MODEL (Pipeline with scaler)
# ==========================================

joblib.dump(pipeline, MODEL_PATH)

print("\n========================================")
print("Model Pipeline Saved Successfully")
print(f"Location : {MODEL_PATH}")
print("========================================")