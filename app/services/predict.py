import joblib
import numpy as np

from pathlib import Path

import tensorflow as tf

from datetime import datetime

from app.services.risk import calculate_risk
from app.services.explain import generate_explanation

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "app" / "model"

# =====================================================
# Load Model
# =====================================================

print("Loading CNN-BiLSTM Model...")

model = tf.keras.models.load_model(
    MODEL_DIR / "cnn_bilstm.keras"
)

print("Model Loaded.")

# =====================================================
# Load Scaler
# =====================================================

print("Loading Scaler...")

scaler = joblib.load(
    MODEL_DIR / "scaler.pkl"
)

print("Scaler Loaded.")

# =====================================================
# Load Encoder
# =====================================================

print("Loading Label Encoder...")

encoder = joblib.load(
    MODEL_DIR / "encoder.pkl"
)

print("Encoder Loaded.")

# =====================================================
# Load Amount Threshold
# =====================================================

print("Loading Amount Threshold...")

amount_threshold = joblib.load(
    MODEL_DIR / "amount_threshold.pkl"
)

print("Threshold Loaded.")

# =====================================================
# Preprocess Single Transaction
# =====================================================

def preprocess_transaction(transaction: dict):

    transaction = transaction.copy()

    # --------------------------------------------
    # Encode transaction type
    # --------------------------------------------

    transaction["type"] = encoder.transform(
        [transaction["type"]]
    )[0]

    # --------------------------------------------
    # Feature Engineering
    # --------------------------------------------

    transaction["originBalanceDiff"] = (
        transaction["oldbalanceOrg"]
        -
        transaction["newbalanceOrig"]
    )

    transaction["destBalanceDiff"] = (
        transaction["newbalanceDest"]
        -
        transaction["oldbalanceDest"]
    )

    transaction["balanceChanged"] = int(
        transaction["originBalanceDiff"] != 0
    )

    transaction["largeTransaction"] = int(
        transaction["amount"] > amount_threshold
    )

    # --------------------------------------------
    # Feature Order
    # --------------------------------------------

    feature_order = [

        "step",

        "type",

        "amount",

        "oldbalanceOrg",

        "newbalanceOrig",

        "oldbalanceDest",

        "newbalanceDest",

        "originBalanceDiff",

        "destBalanceDiff",

        "balanceChanged",

        "largeTransaction"

    ]

    X = np.array(

        [[transaction[col] for col in feature_order]],

        dtype=np.float32

    )

    # --------------------------------------------
    # Scale Numeric Features
    # --------------------------------------------

    numeric_columns = [
        "step",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "originBalanceDiff",
        "destBalanceDiff"
    ]

    feature_index = {
        name: idx
        for idx, name in enumerate(feature_order)
    }

    numeric_indices = [
        feature_index[col]
        for col in numeric_columns
    ]

    X_numeric = X[:, numeric_indices]

    X[:, numeric_indices] = scaler.transform(
        X_numeric
    )

    # --------------------------------------------
    # Reshape
    # --------------------------------------------

    X = X.reshape(

        1,

        X.shape[1],

        1

    )

    return X

# =====================================================
# Calculate Risk Level
# =====================================================

def calculate_risk(probability):

    """
    Calculate risk level based on fraud probability.

    Parameters
    ----------
    probability : float
        Fraud probability (0-1)

    Returns
    -------
    str
        Risk level: "Low", "Medium", or "High"
    """

    if probability < 0.3:
        return "Low"
    elif probability < 0.7:
        return "Medium"
    else:
        return "High"

# =====================================================
# Generate Explanation
# =====================================================

def generate_explanation(transaction):

    """
    Generate explanation for the prediction.

    Parameters
    ----------
    transaction : dict
        Transaction data

    Returns
    -------
    list
        List of explanation reasons
    """

    reasons = []

    if transaction.get("amount", 0) > amount_threshold:
        reasons.append("Large transaction amount")

    if transaction.get("oldbalanceOrg", 0) < transaction.get("amount", 0):
        reasons.append("Insufficient origin balance")

    if transaction.get("type") in ["TRANSFER", "CASH_OUT"]:
        reasons.append("High-risk transaction type")

    return reasons if reasons else ["Standard transaction"]

# =====================================================
# Predict Single Transaction
# =====================================================

def predict_transaction(transaction: dict):

    """
    Predict fraud for a single transaction.

    Parameters
    ----------
    transaction : dict

    Returns
    -------
    dict
    """

    # --------------------------------------------
    # Preprocess
    # --------------------------------------------

    X = preprocess_transaction(transaction)

    # --------------------------------------------
    # Predict Probability
    # --------------------------------------------

    probability = float(

        model.predict(

            X,

            verbose=0

        )[0][0]

    )

    # --------------------------------------------
    # Prediction
    # --------------------------------------------

    prediction = (

        "Fraud"

        if probability >= 0.5

        else

        "Genuine"

    )

    # --------------------------------------------
    # Confidence
    # --------------------------------------------

    confidence = (

        probability

        if prediction == "Fraud"

        else

        1 - probability

    )

    # --------------------------------------------
    # Return Result
    # --------------------------------------------

    from datetime import datetime

    risk = calculate_risk(probability)

    reasons = generate_explanation(transaction)

    return {

    "prediction": prediction,

    "fraud_probability": round(
        probability * 100,
        2
    ),

    "genuine_probability": round(
        (1 - probability) * 100,
        2
    ),

    "confidence": round(
        confidence * 100,
        2
    ),

    "risk_level": risk,

    "timestamp": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),

    "reasons": reasons

}
