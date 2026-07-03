import joblib
import pandas as pd


def load_model(model_path: str):
    return joblib.load(model_path)


def prepare_customer_input(customer_data: dict, model_features: list) -> pd.DataFrame:
    # Create DataFrame
    df = pd.DataFrame([customer_data])

    # Rename columns to match the training data
    df = df.rename(columns={
        "SeniorCitizen": "seniorcitizen",
        "MonthlyCharges": "monthlycharges",
        "TotalCharges": "totalcharges",
        "Partner": "partner",
        "Dependents": "dependents",
        "PhoneService": "phoneservice",
        "MultipleLines": "multiplelines",
        "InternetService": "internetservice",
        "OnlineSecurity": "onlinesecurity",
        "OnlineBackup": "onlinebackup",
        "DeviceProtection": "deviceprotection",
        "TechSupport": "techsupport",
        "StreamingTV": "streamingtv",
        "StreamingMovies": "streamingmovies",
        "Contract": "contract",
        "PaperlessBilling": "paperlessbilling",
        "PaymentMethod": "paymentmethod",
        "gender": "gender"
    })

    # One-hot encode categorical columns
    encoded = pd.get_dummies(df)

    # Create empty feature vector
    feature_vector = pd.DataFrame(0.0, index=[0], columns=model_features)

    # Copy matching columns
    for column in encoded.columns:
        if column in feature_vector.columns:

            value = encoded.loc[0, column]

            if isinstance(value, bool):
                value = int(value)

            feature_vector.loc[0, column] = float(value)
    return feature_vector


def prepare_ltv_input(customer_data: dict, ltv_features: list, churn_prediction: int) -> pd.DataFrame:
    df = pd.DataFrame([customer_data])

    # Convert column names to lowercase
    df.columns = [col.lower() for col in df.columns]

    # One-hot encode
    encoded = pd.get_dummies(df)

    # Create feature vector
    feature_vector = pd.DataFrame(
    0.0,
    index=[0],
    columns=ltv_features
)

    # Copy matching columns
    for column in encoded.columns:
        if column in feature_vector.columns:

            value = encoded.loc[0, column]

            if isinstance(value, bool):
                value = int(value)

            feature_vector.loc[0, column] = float(value)

    # Add churn prediction
    if "churn_Yes" in feature_vector.columns:
        feature_vector.loc[0, "churn_Yes"] = churn_prediction

    return feature_vector