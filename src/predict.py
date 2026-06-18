import joblib
import pandas as pd


def load_model(model_path: str):
    return joblib.load(model_path)


def prepare_customer_input(customer_data: dict, model_features: list) -> pd.DataFrame:
    numeric_features = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
    df = pd.DataFrame([customer_data])
    encoded = pd.get_dummies(df)

    feature_vector = pd.DataFrame(0, index=[0], columns=model_features)

    for feature in numeric_features:
        if feature in df.columns:
            feature_vector.loc[0, feature] = float(df.loc[0, feature])

    for column in encoded.columns:
        if column in feature_vector.columns:
            feature_vector.loc[0, column] = encoded.loc[0, column]

    return feature_vector
