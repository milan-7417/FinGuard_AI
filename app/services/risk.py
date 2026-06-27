# =====================================================
# FinGuard AI
# Risk Assessment
# =====================================================

def calculate_risk(probability):

    """
    probability:
        Value between 0 and 1

    Returns:
        Low / Medium / High
    """

    if probability < 0.30:

        return "Low"

    elif probability < 0.70:

        return "Medium"

    else:

        return "High"