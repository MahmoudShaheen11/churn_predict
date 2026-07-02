import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🏦",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🏦 Customer Churn Prediction System")

col1, col2 = st.columns(2)

with col1:
    credit_score = st.number_input("Credit Score", 300, 900, 650)
    geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", 18, 100, 35)
    tenure = st.number_input("Tenure", 0, 10, 5)

with col2:
    balance = st.number_input("Balance", 0.0, 1e7, 50000.0)
    num_products = st.number_input("Products", 1, 4, 1)
    has_card = st.selectbox("Credit Card", [1, 0])
    active = st.selectbox("Active Member", [1, 0])
    salary = st.number_input("Salary", 0.0, 1e7, 50000.0)

API_URL = "http://api:8000/predict"

if st.button("Predict"):

    data = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": has_card,
        "IsActiveMember": active,
        "EstimatedSalary": salary
    }

    try:
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            result = response.json()

            prob = float(result["probability"])

            st.success(result["prediction"])
            st.metric("Probability", f"{prob*100:.2f}%")

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={"text": "Churn Risk"},
                gauge={"axis": {"range": [0, 100]}}
            ))

            st.plotly_chart(fig)

        else:
            st.error(response.text)

    except Exception as e:
        st.error(f"Connection error: {e}")