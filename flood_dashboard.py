import streamlit as st
import pandas as pd
import numpy as np
#import joblib
import time
import csv
import os

st.set_page_config(page_title="South Lhonak Lake Flood Dashboard", layout="centered")

# Load trained model
model = joblib.load("flood_prediction_model.pkl")

# Log file
csv_file = "flood_logs.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp", "Water_Temperature_C", "Water_Level_m", "Air_Pressure_hPa",
            "Altitude_m", "Seismic_Activity_Richter", "Rainfall_mm", "Air_Temperature_C",
            "Water_Flow_Rate_m3s", "Humidity_percent", "Turbidity_NTU", "Prediction"
        ])

# Fake sensor generator
def get_fake_sensor_data():
    return {
        'Water_Temperature_C': round(np.random.uniform(2, 8), 2),
        'Water_Level_m': round(np.random.uniform(3, 7), 2),
        'Air_Pressure_hPa': round(np.random.uniform(760, 790), 2),
        'Altitude_m': 5200,
        'Seismic_Activity_Richter': round(np.random.uniform(0, 3), 2),
        'Rainfall_mm': round(np.random.uniform(20, 150), 2),
        'Air_Temperature_C': round(np.random.uniform(-5, 15), 2),
        'Water_Flow_Rate_m3s': round(np.random.uniform(1.0, 4.5), 2),
        'Humidity_percent': round(np.random.uniform(50, 100), 2),
        'Turbidity_NTU': round(np.random.uniform(5, 80), 2)
    }

# CSV Logger
def log_to_csv(data_dict, prediction):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp] + list(data_dict.values()) + [prediction])

# App UI
st.title("🌊 South Lhonak Lake Flood Prediction Dashboard")

mode = st.radio("Select Mode", ["Manual Input", "Sensor Mode (Simulated)"])

# === Manual Mode ===
if mode == "Manual Input":
    st.subheader("✍️ Enter Sensor Values Manually")

    with st.form("manual_form"):
        water_temp = st.number_input("Water Temperature (°C)", value=5.0)
        water_level = st.number_input("Water Level (m)", value=5.5)
        air_pressure = st.number_input("Air Pressure (hPa)", value=775.0)
        altitude = st.number_input("Altitude (m)", value=5200)
        seismic = st.number_input("Seismic Activity (Richter)", value=0.5)
        rainfall = st.number_input("Rainfall (mm)", value=50.0)
        air_temp = st.number_input("Air Temperature (°C)", value=5.0)
        flow_rate = st.number_input("Water Flow Rate (m³/s)", value=2.0)
        humidity = st.number_input("Humidity (%)", value=70.0)
        turbidity = st.number_input("Turbidity (NTU)", value=25.0)

        submit = st.form_submit_button("🔍 Predict Flood Risk")

    if submit:
        input_data = {
            'Water_Temperature_C': water_temp,
            'Water_Level_m': water_level,
            'Air_Pressure_hPa': air_pressure,
            'Altitude_m': altitude,
            'Seismic_Activity_Richter': seismic,
            'Rainfall_mm': rainfall,
            'Air_Temperature_C': air_temp,
            'Water_Flow_Rate_m3s': flow_rate,
            'Humidity_percent': humidity,
            'Turbidity_NTU': turbidity
        }

        prediction = model.predict([list(input_data.values())])[0]

        st.subheader("🧠 Prediction Result")
        if prediction == 1:
            st.error("⚠️ FLOOD RISK DETECTED")
        else:
            st.success("✅ No Flood Risk")

        log_to_csv(input_data, prediction)

# === Sensor Mode ===
else:
    st.subheader("📡 Live Sensor Mode (Simulated)")
    placeholder = st.empty()
    history = []

    run = st.checkbox("Start Sensor Simulation")

    if run:
        while True:
            sensor_data = get_fake_sensor_data()
            prediction = model.predict([list(sensor_data.values())])[0]
            log_to_csv(sensor_data, prediction)

            history.append({
                "Time": time.strftime("%H:%M:%S"),
                "Water Level": sensor_data['Water_Level_m'],
                "Flow Rate": sensor_data['Water_Flow_Rate_m3s'],
                "Turbidity": sensor_data['Turbidity_NTU']
            })
            if len(history) > 50:
                history.pop(0)

            df_history = pd.DataFrame(history)

            with placeholder.container():
                st.write("### 🔢 Latest Sensor Readings")
                st.write(pd.DataFrame([sensor_data]))

                st.write("### 🧠 ML Prediction")
                if prediction == 1:
                    st.error("⚠️ FLOOD RISK DETECTED")
                else:
                    st.success("✅ No Flood Risk")

                st.write("### 📈 Live Graphs")
                st.line_chart(df_history.set_index("Time"))

            time.sleep(3)
