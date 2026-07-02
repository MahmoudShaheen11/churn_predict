import streamlit as st
import requests
import plotly.graph_objects as go

# ---------------------- Page Config ----------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- Session State (History) ----------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------- Sidebar ----------------------
with st.sidebar:
    st.title("🏦 Churn Prediction")

    st.markdown("---")

    st.markdown("""
## Model Information

**Model:** Random Forest  
**Backend:** FastAPI  
**Frontend:** Streamlit  
**Language:** Python  
**Task:** Customer Churn Prediction
""")

    st.markdown("---")

    st.info(
        "This application predicts whether a bank customer is likely to leave the bank."
    )

# ---------------------- Title ----------------------
st.title("🏦 Customer Churn Prediction System")

st.caption(
    "Machine Learning End-to-End Project using Random Forest + FastAPI + Streamlit"
)

st.markdown("---")

st.subheader("📋 Customer Information")

# ---------------------- Inputs ----------------------
col1, col2 = st.columns(2)

with col1:

    credit_score = st.number_input("Credit Score", 300, 900, 650)

    geography = st.selectbox("Geography", ["France", "Germany", "Spain"])

    gender = st.selectbox("Gender", ["Male", "Female"])

    age = st.number_input("Age", 18, 100, 35)

    tenure = st.number_input("Tenure", 0, 10, 5)

with col2:

    balance = st.number_input("Balance", min_value=0.0, value=50000.0)

    num_products = st.number_input("Number of Products", 1, 4, 1)

    has_card = st.selectbox("Has Credit Card", [1, 0])

    active_member = st.selectbox("Is Active Member", [1, 0])

    salary = st.number_input("Estimated Salary", min_value=0.0, value=50000.0)

st.markdown("---")

predict_button = st.button("🚀 Predict", use_container_width=True)

# ---------------------- Prediction ----------------------
if predict_button:

    customer = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": has_card,
        "IsActiveMember": active_member,
        "EstimatedSalary": salary
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=customer
        )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]
            probability = float(result["probability"])

            # ---------------- Gauge Chart ----------------
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                number={"suffix": "%"},
                title={"text": "Churn Risk"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, 40], "color": "lightgreen"},
                        {"range": [40, 70], "color": "gold"},
                        {"range": [70, 100], "color": "tomato"}
                    ]
                }
            ))

            fig.update_layout(height=300)

            # ---------------- Result ----------------
            st.markdown("---")
            st.subheader("📊 Prediction Result")

            col1, col2 = st.columns([1, 1])

            with col1:

                if prediction == "Churn":
                    st.error("🔴 Customer is likely to Churn")
                else:
                    st.success("🟢 Customer is NOT likely to Churn")

                st.metric(
                    "Churn Probability",
                    f"{probability*100:.2f}%"
                )

                st.progress(probability)

            with col2:
                st.plotly_chart(fig, use_container_width=True)

            # ---------------- Save History ----------------
            st.session_state.history.append({
                "Credit Score": credit_score,
                "Age": age,
                "Country": geography,
                "Prediction": prediction,
                "Probability": f"{probability*100:.2f}%"
            })

            # ---------------- Details ----------------
            st.markdown("---")
            st.subheader("📄 Prediction Details")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Customer Information")
                st.write(f"**Credit Score:** {credit_score}")
                st.write(f"**Age:** {age}")
                st.write(f"**Country:** {geography}")
                st.write(f"**Gender:** {gender}")
                st.write(f"**Tenure:** {tenure}")

            with col2:
                st.write("### Account Information")
                st.write(f"**Balance:** ${balance:,.2f}")
                st.write(f"**Products:** {num_products}")
                st.write(f"**Credit Card:** {'Yes' if has_card else 'No'}")
                st.write(f"**Active Member:** {'Yes' if active_member else 'No'}")
                st.write(f"**Salary:** ${salary:,.2f}")

            with st.expander("🔍 Raw API Response"):
                st.json(result)

        else:
            st.error("API Error")
            st.code(response.text)

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to FastAPI Server.")
        st.info("Start FastAPI first:")
        st.code("uvicorn app.main:app --reload")

# ---------------------- History Section ----------------------
st.markdown("---")
st.subheader("📜 Prediction History")

if len(st.session_state.history) > 0:
    st.dataframe(st.session_state.history[::-1])
else:
    st.info("No predictions yet.")

# ---------------------- Clear History ----------------------
if st.button("🗑️ Clear History"):
    st.session_state.history = []
    st.rerun()