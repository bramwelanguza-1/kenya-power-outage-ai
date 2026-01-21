import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Kenya Power Outage Predictor")

@st.cache_data
def load_data():
    return pd.read_excel("Kenya_Power_Outage_Estimated_Data.xlsx")

df = load_data()

df['Date'] = pd.to_datetime(df['Date'])
df['Hour'] = pd.to_datetime(df['Time']).dt.hour
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month
df['Rain'] = df['Rain'].map({'Yes': 1, 'No': 0})
df['Location_Code'] = df['Location'].astype('category').cat.codes

X = df[['Hour', 'DayOfWeek', 'Month', 'Rain', 'Location_Code']]
y = df['Outage_Occurred']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

st.title("⚡ Kenya Power Outage Risk Predictor")

location = st.selectbox("Location", df['Location'].unique())
hour = st.slider("Hour of Day", 0, 23, 18)
day = st.slider("Day of Week (0=Monday)", 0, 6, 2)
month = st.slider("Month", 1, 12, 3)
rain = st.selectbox("Is it raining?", ["Yes", "No"])

location_code = df[df['Location'] == location]['Location_Code'].iloc[0]
rain_val = 1 if rain == "Yes" else 0

if st.button("Predict Outage Risk"):
    risk = model.predict_proba([[hour, day, month, rain_val, location_code]])[0][1]
    st.metric("Outage Risk (%)", f"{round(risk * 100, 2)}%")

    if risk > 0.6:
        st.warning("⚠️ High outage risk. Prepare backup power.")
    else:
        st.success("✅ Low outage risk. Normal operation expected.")
