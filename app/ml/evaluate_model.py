"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: evaluate_model.py
Purpose: Evaluate Trained Random Forest Model
----------------------------------------------------------
"""

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "processed_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "saved_models",
    "dropout_model.pkl"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

os.makedirs(REPORT_DIR, exist_ok=True)

REPORT_FILE = os.path.join(
    REPORT_DIR,
    "accuracy_report.txt"
)

CONFUSION_IMAGE = os.path.join(
    REPORT_DIR,
    "confusion_matrix.png"
)

# ==========================================
# LOAD MODEL
# ==========================================

print("\nLoading trained model...")

model = joblib.load(MODEL_PATH)

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(DATASET_PATH)

X = df.drop(
    columns=[
        "student_id",
        "dropout"
    ]
)

y = df["dropout"]

# ==========================================
# PREDICT
# ==========================================

predictions = model.predict(X)

accuracy = accuracy_score(
    y,
    predictions
)

report = classification_report(
    y,
    predictions
)

matrix = confusion_matrix(
    y,
    predictions
)

# ==========================================
# SAVE REPORT
# ==========================================

with open(REPORT_FILE, "w") as file:

    file.write("AI Dropout Prediction Model Evaluation\n")
    file.write("=" * 50)
    file.write("\n\n")

    file.write(f"Accuracy : {accuracy * 100:.2f}%\n\n")

    file.write("Classification Report\n")
    file.write("----------------------------\n")
    file.write(report)

print("\nAccuracy report saved.")

# ==========================================
# SAVE CONFUSION MATRIX IMAGE
# ==========================================

disp = ConfusionMatrixDisplay(
    confusion_matrix=matrix
)

disp.plot()

plt.title("Confusion Matrix")

plt.savefig(
    CONFUSION_IMAGE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Confusion matrix image saved.")

# ==========================================
# SUMMARY
# ==========================================

print("\n====================================")
print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Report    : {REPORT_FILE}")
print(f"Image     : {CONFUSION_IMAGE}")
print("====================================")