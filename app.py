import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kenya Power Outage Predictor", layout="centered")

@st.cache_data
def load_data():
    return pd.read_excel("Kenya_Power_Outage_Estimated_Data.xlsx")

df = load_data()

df['Date'] = pd.to_datetime(df['Date'])
df['Hour'] = pd.to_datetime(df['Time']).dt.hour
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month

st.title("⚡ Kenya Power Outage Risk Predictor")
st.caption("AI-assisted outage risk estimation for Kenya")

location = st.selectbox("Location", df['Location'].unique())
hour = st.slider("Hour of Day", 0, 23, 18)
day = st.slider("Day of Week (0=Monday)", 0, 6, 2)
month = st.slider("Month", 1, 12, 3)
rain = st.selectbox("Is it raining?", ["Yes", "No"])

# ---- Lightweight risk engine (NO sklearn) ----
risk = 0.15

if rain == "Yes":
    risk += 0.25
if hour in range(18, 23):
    risk += 0.30
if day in [4, 5]:
    risk += 0.10
if location in df['Location'].value_counts().head(3).index:
    risk += 0.10

risk = min(risk, 0.95)

if st.button("Predict Outage Risk"):
    st.metric("Estimated Outage Risk", f"{int(risk * 100)}%")

    if risk >= 0.65:
        st.warning("⚠️ High risk. Prepare backup power.")
    elif risk >= 0.40:
        st.info("ℹ️ Moderate risk. Stay alert.")
    else:
        st.success("✅ Low risk. Normal operation expected.")
