# =====================================================
# FinGuard AI
# Model Evaluation
# =====================================================

import json
import joblib
import numpy as np

from pathlib import Path

import tensorflow as tf

import matplotlib.pyplot as plt

from sklearn.metrics import (

    classification_report,

    confusion_matrix,

    ConfusionMatrixDisplay,

    roc_curve,

    auc,

    precision_recall_curve,

    average_precision_score,

    precision_score,

    recall_score,

    accuracy_score,

    f1_score

)

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = BASE_DIR / "app" / "model"

ARTIFACT_DIR = BASE_DIR / "training" / "artifacts"

RESULT_DIR = BASE_DIR / "training" / "results"

RESULT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# Load Model
# =====================================================

print("=" * 60)
print("Loading CNN + BiLSTM Model")
print("=" * 60)

model = tf.keras.models.load_model(

    MODEL_DIR / "cnn_bilstm.keras"

)

print("Model Loaded Successfully.\n")

# =====================================================
# Load Test Dataset
# =====================================================

print("=" * 60)
print("Loading Test Dataset")
print("=" * 60)

X_test = np.load(

    ARTIFACT_DIR / "X_test.npy"

)

y_test = np.load(

    ARTIFACT_DIR / "y_test.npy"

)

print("Test Dataset Loaded.")

print("\nShape")

print("X_test :", X_test.shape)

print("y_test :", y_test.shape)

# =====================================================
# Load Training History
# =====================================================

history = joblib.load(

    ARTIFACT_DIR / "history.pkl"

)

print("\nTraining History Loaded.")

# =====================================================
# Prediction
# =====================================================

print("\n")
print("=" * 60)
print("Running Prediction...")
print("=" * 60)

y_prob = model.predict(
    X_test,
    verbose=1
)


y_prob = y_prob.ravel()
y_pred = (y_prob >= 0.5).astype(int)

print("\nPrediction Completed.")

# =====================================================
# Evaluation Metrics
# =====================================================

accuracy = accuracy_score(

    y_test,

    y_pred

)

precision = precision_score(

    y_test,

    y_pred

)

recall = recall_score(

    y_test,

    y_pred

)

f1 = f1_score(

    y_test,

    y_pred

)

roc_auc = average_precision_score(

    y_test,

    y_prob

)

# =====================================================
# Classification Report
# =====================================================

print("\n")

print("=" * 60)

print("Classification Report")

print("=" * 60)

print(

    classification_report(

        y_test,

        y_pred,

        digits=4

    )

)

# =====================================================
# Confusion Matrix
# =====================================================

cm = confusion_matrix(

    y_test,

    y_pred

)

disp = ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=["Genuine","Fraud"]

)

plt.figure(figsize=(7,6))

disp.plot(

    cmap="Blues",

    values_format="d"

)

plt.title("Confusion Matrix")

plt.savefig(

    RESULT_DIR / "confusion_matrix.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

# =====================================================
# ROC Curve
# =====================================================

fpr, tpr, _ = roc_curve(

    y_test,

    y_prob

)

roc_score = auc(

    fpr,

    tpr

)

plt.figure(figsize=(7,6))

plt.plot(

    fpr,

    tpr,

    linewidth=2,

    label=f"AUC = {roc_score:.4f}"

)

plt.plot(

    [0,1],

    [0,1],

    linestyle="--"

)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()

plt.grid(True)

plt.savefig(

    RESULT_DIR / "roc_curve.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

# =====================================================
# Precision Recall Curve
# =====================================================

precision_curve, recall_curve, _ = precision_recall_curve(

    y_test,

    y_prob

)

average_precision = average_precision_score(

    y_test,

    y_prob

)

plt.figure(figsize=(7,6))

plt.plot(

    recall_curve,

    precision_curve,

    linewidth=2,

    label=f"AP = {average_precision:.4f}"

)

plt.xlabel("Recall")

plt.ylabel("Precision")

plt.title("Precision Recall Curve")

plt.legend()

plt.grid(True)

plt.savefig(

    RESULT_DIR / "precision_recall_curve.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

# =====================================================
# Save Metrics
# =====================================================

metrics = {

    "Accuracy": float(accuracy),

    "Precision": float(precision),

    "Recall": float(recall),

    "F1 Score": float(f1),

    "ROC AUC": float(roc_score),

    "Average Precision": float(average_precision)

}

with open(

    RESULT_DIR / "metrics.json",

    "w"

) as file:

    json.dump(

        metrics,

        file,

        indent=4

    )

print("\nMetrics Saved Successfully.")

