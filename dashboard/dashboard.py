import streamlit as st
import pandas as pd
import joblib
import os

# Page Configuration
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Customer Churn Prediction System")
st.markdown("### Machine Learning Powered Customer Retention Analytics")
st.markdown("---")

# Load data from PostgreSQL
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_churn_data

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

try:
    df_dashboard = get_churn_data()

except Exception as e:
    st.error(f"⚠️ Could not connect to PostgreSQL. Using CSV fallback: {e}")

    DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "processed_churn_data.csv"
    )

    df_dashboard = pd.read_csv(DATA_PATH)

# =========================
# OVERVIEW
# =========================
st.subheader("📈 Churn Overview")

churn_counts = df_dashboard["churn"].value_counts()

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(churn_counts)

with col2:
    st.write("Churn Distribution")
    st.dataframe(churn_counts)

# =========================
# KPI METRICS
# =========================
st.subheader("📊 Key Business Metrics")

col1, col2, col3, col4 = st.columns(4)

total_customers = len(df_dashboard)
churned = len(df_dashboard[df_dashboard["churn"] == "Yes"])
retained = len(df_dashboard[df_dashboard["churn"] == "No"])
churn_rate = (churned / total_customers) * 100

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned)
col3.metric("Retained Customers", retained)
col4.metric("Churn Rate", f"{churn_rate:.2f}%")

# =========================
# INSIGHTS
# =========================
st.subheader("🔍 Key Business Insights")

st.info("📌 Month-to-month customers are most likely to churn")
st.info("📌 Fiber optic users show higher churn risk")
st.info("📌 Long tenure customers are more loyal")
st.info("📌 Higher monthly charges increase churn probability")

# =========================
# MODEL
# =========================
MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_rf_model.pkl")
model = joblib.load(MODEL_PATH)
model_features = list(model.feature_names_in_)

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("Customer Details")

senior = st.sidebar.selectbox("Senior Citizen", [0, 1])
tenure = st.sidebar.slider("Tenure", 0, 72, 12)
monthly = st.sidebar.number_input("Monthly Charges", 0.0, 200.0, 70.0)
total = st.sidebar.number_input("Total Charges", 0.0, 10000.0, 1000.0)

# =========================
# PREDICTION
# =========================
if st.sidebar.button("Predict"):

    customer_dict = {
        'SeniorCitizen': senior,
        'tenure': tenure,
        'MonthlyCharges': monthly,
        'TotalCharges': total,
        'gender': 'Male',
        'Partner': 'No',
        'Dependents': 'No',
        'PhoneService': 'No',
        'MultipleLines': 'No phone service',
        'InternetService': 'DSL',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check'
    }

    from src.predict import prepare_customer_input

    input_data = prepare_customer_input(customer_dict, model_features)

    st.write("Input sent to model:")
    st.dataframe(input_data)

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    churn_prob = probability[0][1] * 100

    st.subheader("🎯 Prediction Result")

    if prediction[0] == 1:
        st.error("🚨 High Risk: Customer is Likely to Churn")
        st.markdown("**Recommendation:** Offer retention discounts or support plan.")
    else:
        st.success("✅ Low Risk: Customer is Likely to Stay")
        st.markdown("**Recommendation:** Maintain service quality to retain customer.")

    st.write(f"Churn Probability: {churn_prob:.2f}%")
    st.progress(min(int(churn_prob), 100))