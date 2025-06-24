import streamlit as st
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie

# Set page config
st.set_page_config(
    page_title="Fraud Detector",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load animation from Lottie URL
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

lottie_ai = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_2glqweqs.json")

# Load model
model = joblib.load("fraud_detection_pipeline.pkl")

# Add background styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #00c6ff	 ;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and animation
st.title("💳 Fraud Detection")
st.markdown("Enter the transaction details below and let AI detect potential fraud in real-time.")

if lottie_ai:
    st_lottie(lottie_ai, height=300, key="ai-animation")
else:
    st.warning("⚠️ Unable to load animation. Check internet or URL.")

st.divider()

# Input fields
transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"])
amount = st.number_input("💰 Amount", min_value=100.0, step=100.0)
oldbalanceOrg = st.number_input("🏦 Old Balance (Sender)", min_value=0.0, value=10000.0)
newbalanceOrg = st.number_input("🏦 New Balance (Sender)", min_value=0.0, value=9000.0)
oldbalanceDest = st.number_input("🏧 Old Balance (Receiver)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("🏧 New Balance (Receiver)", min_value=0.0, value=0.0)

# Predict button
if st.button("🚀 Predict"):
    input_data = pd.DataFrame({
        "type": [transaction_type],
        "amount": [amount],
        "oldbalanceOrg": [oldbalanceOrg],
        "newbalanceOrig": [newbalanceOrg],
        "oldbalanceDest": [oldbalanceDest],
        "newbalanceDest": [newbalanceDest]
    })

    prediction = model.predict(input_data)[0]

    st.subheader(f"Prediction: {int(prediction)}")

    if prediction == 1:
        st.error("⚠️ This transaction might be **fraudulent**.")
    else:
        st.success("✅ This transaction looks **safe**.")

st.divider()

st.markdown("👨‍💻 The project is done by [JANARTHANAN](https://www.linkedin.com/in/janarthanan-s-130058304?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)")
