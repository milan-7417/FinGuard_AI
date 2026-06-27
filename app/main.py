from pathlib import Path
import pandas as pd

from fastapi import UploadFile, File

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from app.services.predict import predict_transaction


# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(

    title="FinGuard AI",

    description="AI Powered Financial Fraud Detection System",

    version="1.0.0"

)


# =====================================================
# Static Files
# =====================================================

STATIC_DIR = Path(__file__).parent / "static"

app.mount(

    "/static",

    StaticFiles(directory=STATIC_DIR),

    name="static"

)


# =====================================================
# Input Schema
# =====================================================

class Transaction(BaseModel):

    step: int

    type: str

    amount: float

    oldbalanceOrg: float

    newbalanceOrig: float

    oldbalanceDest: float

    newbalanceDest: float


# =====================================================
# Landing Page
# =====================================================

@app.get("/")

def landing():

    return FileResponse(

        STATIC_DIR / "landing.html"

    )


# =====================================================
# Dashboard
# =====================================================

@app.get("/dashboard")

def dashboard():

    return FileResponse(

        STATIC_DIR / "dashboard.html"

    )


# =====================================================
# Prediction API
# =====================================================

@app.post("/predict")

def predict(data: Transaction):

    result = predict_transaction(

        data.model_dump()

    )

    return result

# =====================================================
# CSV Prediction
# =====================================================

@app.post("/predict-csv")
async def predict_csv(

    file: UploadFile = File(...)

):

    try:

        df = pd.read_csv(

            file.file

        )

        results = []

        for _, row in df.iterrows():

            transaction = {

                "step": int(row["step"]),

                "type": str(row["type"]),

                "amount": float(row["amount"]),

                "oldbalanceOrg": float(row["oldbalanceOrg"]),

                "newbalanceOrig": float(row["newbalanceOrig"]),

                "oldbalanceDest": float(row["oldbalanceDest"]),

                "newbalanceDest": float(row["newbalanceDest"])

            }

            prediction = predict_transaction(

                transaction

            )

            results.append(

                prediction

            )

        return {

            "total_transactions": len(results),

            "results": results

        }

    except Exception as e:

        return {

            "error": str(e)

        }


# =====================================================
# Health Check
# =====================================================

@app.get("/health")

def health():

    return {

        "status": "running",

        "model": "CNN + BiLSTM"

    }