import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from database.db import get_all_appointments


def predict(monthly_df):
    st.subheader("🤖 Revenue Prediction")

    if monthly_df is None or monthly_df.empty or len(monthly_df) < 2:
        st.info("Not enough revenue data for prediction.")
        return

    monthly_df = monthly_df.copy()
    monthly_df["Month_Num"] = np.arange(len(monthly_df))

    X = monthly_df[["Month_Num"]]
    y = monthly_df["Revenue"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    future = np.array([[len(monthly_df) + i] for i in range(1, 4)])
    predictions = model.predict(future)

    st.write("### Next 3 Months Revenue Forecast")
    for i, value in enumerate(predictions, start=1):
        st.write(f"Month {i}: ₹{value:,.0f}")

    pred_df = pd.DataFrame({
        "Future_Month": [f"Month {i}" for i in range(1, 4)],
        "Predicted_Revenue": predictions
    })
    st.line_chart(pred_df.set_index("Future_Month"))


def predict_appointments():
    st.subheader("📅 Appointment Volume Forecast")

    appointments_df = get_all_appointments()
    if appointments_df.empty or len(appointments_df) < 2:
        st.info("Not enough appointment data for forecast.")
        return

    appointments_df = appointments_df.copy()
    appointments_df["appointment_date"] = pd.to_datetime(appointments_df["appointment_date"], errors="coerce")
    appointments_df["Month"] = appointments_df["appointment_date"].dt.to_period("M").astype(str)

    monthly_counts = appointments_df.groupby("Month").size().reset_index(name="Appointments")
    if len(monthly_counts) < 2:
        st.info("Not enough monthly appointment data.")
        return

    monthly_counts["Month_Num"] = np.arange(len(monthly_counts))
    X = monthly_counts[["Month_Num"]]
    y = monthly_counts["Appointments"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    future = np.array([[len(monthly_counts) + i] for i in range(1, 4)])
    predictions = model.predict(future)

    for i, value in enumerate(predictions, start=1):
        st.write(f"Month {i} predicted appointments: {round(value)}")

    pred_df = pd.DataFrame({
        "Future_Month": [f"Month {i}" for i in range(1, 4)],
        "Predicted_Appointments": predictions
    })
    st.line_chart(pred_df.set_index("Future_Month"))