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

# Dataset Path Fix
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed_churn_data.csv")

df_dashboard = pd.read_csv(DATA_PATH)

# =========================
# OVERVIEW
# =========================
st.subheader("📈 Churn Overview")

churn_counts = df_dashboard["Churn"].value_counts()

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
churned = len(df_dashboard[df_dashboard["Churn"] == "Yes"])
retained = len(df_dashboard[df_dashboard["Churn"] == "No"])
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

    input_data = pd.DataFrame({
        'SeniorCitizen': [senior],
        'tenure': [tenure],
        'MonthlyCharges': [monthly],
        'TotalCharges': [total]
    })

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