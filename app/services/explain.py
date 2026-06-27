# =====================================================
# FinGuard AI
# Explanation Engine
# =====================================================

import joblib

from pathlib import Path


# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "app" / "model"


# =====================================================
# Load Amount Threshold
# =====================================================

amount_threshold = joblib.load(
    MODEL_DIR / "amount_threshold.pkl"
)


# =====================================================
# Generate Explanation
# =====================================================

def generate_explanation(transaction):

    """
    Generate human-readable explanations
    for the prediction.
    """

    reasons = []

    # --------------------------------------------
    # High Transaction Amount
    # --------------------------------------------

    if transaction["amount"] > amount_threshold:

        reasons.append(
            f"Transaction amount is unusually high (>{amount_threshold:.2f})."
        )

    # --------------------------------------------
    # Transaction Type
    # --------------------------------------------

    if transaction["type"] in [

        "TRANSFER",

        "CASH_OUT"

    ]:

        reasons.append(
            f"Transaction type is '{transaction['type']}', which is commonly associated with fraudulent activity."
        )

    # --------------------------------------------
    # Origin Balance Difference
    # --------------------------------------------

    origin_diff = (

        transaction["oldbalanceOrg"]

        -

        transaction["newbalanceOrig"]

    )

    if origin_diff > amount_threshold:

        reasons.append(
            "Large decrease detected in the origin account balance."
        )

    # --------------------------------------------
    # Destination Balance Difference
    # --------------------------------------------

    dest_diff = (

        transaction["newbalanceDest"]

        -

        transaction["oldbalanceDest"]

    )

    if dest_diff > amount_threshold:

        reasons.append(
            "Large increase detected in the destination account balance."
        )

    # --------------------------------------------
    # Zero Balance Anomaly
    # --------------------------------------------

    if (

        transaction["oldbalanceOrg"] > 0

        and

        transaction["newbalanceOrig"] == 0

    ):

        reasons.append(
            "Origin account balance became zero immediately after the transaction."
        )

    # --------------------------------------------
    # Empty Destination Account
    # --------------------------------------------

    if (

        transaction["oldbalanceDest"] == 0

        and

        transaction["newbalanceDest"] > amount_threshold

    ):

        reasons.append(
            "Destination account previously had zero balance before receiving a large transaction."
        )

    # --------------------------------------------
    # Large Transaction Flag
    # --------------------------------------------

    if transaction["amount"] > amount_threshold:

        reasons.append(
            "Transaction exceeds the learned high-value transaction threshold."
        )

    # --------------------------------------------
    # Default
    # --------------------------------------------

    if len(reasons) == 0:

        reasons.append(
            "No significant fraud indicators were identified."
        )

    return reasons


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    sample = {

        "type": "TRANSFER",

        "amount": 500000,

        "oldbalanceOrg": 600000,

        "newbalanceOrig": 100000,

        "oldbalanceDest": 10000,

        "newbalanceDest": 510000

    }

    explanation = generate_explanation(sample)

    print("\nFraud Explanation\n")

    for reason in explanation:

        print(f"• {reason}")