from fastapi import FastAPI
from pydantic import BaseModel, Field
import os
from src.predict import load_model, prepare_customer_input

app = FastAPI(title="Customer Churn API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_rf_model.pkl")
model = load_model(MODEL_PATH)
model_features = list(model.feature_names_in_)


class CustomerPayload(BaseModel):
    SeniorCitizen: int = Field(..., ge=0, le=1, description="0 for non-senior, 1 for senior citizen")
    tenure: int = Field(..., ge=0, le=72)
    MonthlyCharges: float = Field(..., ge=0.0)
    TotalCharges: float = Field(..., ge=0.0)
    gender: str = Field("Male")
    Partner: str = Field("No")
    Dependents: str = Field("No")
    PhoneService: str = Field("No")
    MultipleLines: str = Field("No phone service")
    InternetService: str = Field("DSL")
    OnlineSecurity: str = Field("No")
    OnlineBackup: str = Field("No")
    DeviceProtection: str = Field("No")
    TechSupport: str = Field("No")
    StreamingTV: str = Field("No")
    StreamingMovies: str = Field("No")
    Contract: str = Field("Month-to-month")
    PaperlessBilling: str = Field("Yes")
    PaymentMethod: str = Field("Electronic check")


@app.get("/")
def root():
    return {"message": "Customer Churn API is running"}


@app.post("/predict")
def predict_churn(payload: CustomerPayload):
    customer_data = payload.dict()
    input_df = prepare_customer_input(customer_data, model_features)
    prediction = model.predict(input_df)[0]
    probability = float(model.predict_proba(input_df)[0][1])
    return {
        "prediction": int(prediction),
        "churn_probability": round(probability * 100, 2),
        "status": "Churn" if prediction == 1 else "Retain"
    }
