from fastapi import FastAPI
from pydantic import BaseModel, Field
import os
import joblib

from src.predict import (
    load_model,
    prepare_customer_input,
    prepare_ltv_input
)
from src.database import get_churn_summary

app = FastAPI(title="Customer Churn API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_rf_model.pkl")
model = load_model(MODEL_PATH)

LTV_MODEL_PATH = os.path.join(BASE_DIR, "models", "ltv_rf_model.pkl")
LTV_SCALER_PATH = os.path.join(BASE_DIR, "models", "ltv_scaler.pkl")

ltv_model = joblib.load(LTV_MODEL_PATH)
ltv_scaler = joblib.load(LTV_SCALER_PATH)

LTV_FEATURES_PATH = os.path.join(BASE_DIR, "models", "ltv_features.txt")

with open(LTV_FEATURES_PATH, "r") as f:
    ltv_features = [line.strip() for line in f]

model_features = list(model.feature_names_in_)


class CustomerPayload(BaseModel):
    SeniorCitizen: int = Field(..., ge=0, le=1)
    tenure: int = Field(..., ge=0, le=72)
    MonthlyCharges: float = Field(..., ge=0.0)
    TotalCharges: float = Field(..., ge=0.0)
    gender: str = "Male"
    Partner: str = "No"
    Dependents: str = "No"
    PhoneService: str = "No"
    MultipleLines: str = "No phone service"
    InternetService: str = "DSL"
    OnlineSecurity: str = "No"
    OnlineBackup: str = "No"
    DeviceProtection: str = "No"
    TechSupport: str = "No"
    StreamingTV: str = "No"
    StreamingMovies: str = "No"
    Contract: str = "Month-to-month"
    PaperlessBilling: str = "Yes"
    PaymentMethod: str = "Electronic check"


@app.get("/")
def root():
    return {"message": "Customer Churn API is running"}


@app.get("/stats")
def get_stats():
    try:
        stats = get_churn_summary()
        return {"status": "success", "data": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/predict")
def predict_churn(payload: CustomerPayload):
    try:
        customer_data = payload.dict()

        input_df = prepare_customer_input(customer_data, model_features)

        prediction = model.predict(input_df)[0]

        probability = float(model.predict_proba(input_df)[0][1])

        prediction_int = 1 if prediction == "Yes" else 0

        return {
            "prediction": prediction_int,
            "churn_probability": round(probability * 100, 2),
            "status": "Churn" if prediction == "Yes" else "Retain"
        }

    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.post("/predict_ltv")
def predict_ltv(payload: CustomerPayload):

    customer_data = payload.dict()

    # Step 1: Predict churn
    churn_input = prepare_customer_input(customer_data, model_features)

    prediction = model.predict(churn_input)[0]

    churn_prediction = 1 if prediction == "Yes" else 0

    # Step 2: Prepare LTV input
    ltv_input = prepare_ltv_input(
        customer_data,
        ltv_features,
        churn_prediction
    )

    # Step 3: Predict LTV
    predicted_ltv = float(ltv_model.predict(ltv_input)[0])

    return {
        "predicted_ltv": round(predicted_ltv, 2)
    }