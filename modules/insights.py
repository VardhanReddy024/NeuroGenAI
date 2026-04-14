import streamlit as st
import pandas as pd
from database.db import get_all_appointments, get_doctor_profiles


def _card(title, value, color="#00E5A8"):
    return f"""
    <div style="
        background: rgba(255,255,255,0.05);
        border-left: 4px solid {color};
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
    ">
        <div style="font-size:14px; color:#CBD5E1;">{title}</div>
        <div style="font-size:20px; font-weight:700; color:#F8FAFC;">{value}</div>
    </div>
    """


def show_insights(df):
    st.subheader("Insights")

    if df.empty:
        st.info("No data available for insights.")
        return

    work_df = df.copy()

    if "Profit" not in work_df.columns:
        work_df["Profit"] = work_df["Revenue"] - work_df["Expense"]

    work_df["Month"] = pd.to_datetime(
        work_df["Admission_Date"], errors="coerce"
    ).dt.to_period("M").astype(str)

    top_department_patients = work_df["Department"].value_counts().idxmax()
    top_department_revenue = work_df.groupby("Department")["Revenue"].sum().idxmax()
    top_department_profit = work_df.groupby("Department")["Profit"].sum().idxmax()

    busiest_doctor = "N/A"
    if "Doctor_Name" in work_df.columns:
        busiest_doctor = work_df["Doctor_Name"].value_counts().idxmax()

    monthly = work_df.groupby("Month")["Revenue"].sum().reset_index()
    avg_growth = "Not enough data"
    growth_value = None

    if len(monthly) > 1:
        growth_value = monthly["Revenue"].pct_change().mean() * 100
        avg_growth = f"{growth_value:.2f}%"

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(_card("Highest Patient Load Department", top_department_patients, "#38BDF8"), unsafe_allow_html=True)
        st.markdown(_card("Highest Revenue Department", top_department_revenue, "#00E5A8"), unsafe_allow_html=True)

    with c2:
        st.markdown(_card("Best Profit Department", top_department_profit, "#F59E0B"), unsafe_allow_html=True)
        st.markdown(_card("Busiest Doctor", busiest_doctor, "#A78BFA"), unsafe_allow_html=True)

    st.markdown(_card("Average Monthly Revenue Growth", avg_growth, "#10B981"), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Notifications")

    appointments_df = get_all_appointments()
    doctor_df = get_doctor_profiles()

    if not appointments_df.empty:
        today = pd.Timestamp.today().strftime("%Y-%m-%d")
        todays_count = len(appointments_df[appointments_df["appointment_date"] == today])
        cancelled_count = len(appointments_df[appointments_df["status"] == "Cancelled"])
        booked_count = len(appointments_df[appointments_df["status"] == "Booked"])

        st.info(f"Today's appointments: {todays_count}")
        st.warning(f"Cancelled appointments: {cancelled_count}")
        st.success(f"Currently booked appointments: {booked_count}")

    if not doctor_df.empty:
        available_count = len(doctor_df[doctor_df["doctor_status"] == "Available"])
        st.info(f"Available doctors: {available_count}")

    total_revenue = work_df["Revenue"].sum()
    total_expense = work_df["Expense"].sum()

    if total_expense > total_revenue:
        st.error("Expense is higher than revenue for the selected filters.")
    else:
        st.success("Revenue is healthy compared to expense.")

    if growth_value is not None:
        if growth_value > 0:
            st.success(f"Revenue trend is growing by {growth_value:.2f}%.")
        elif growth_value < 0:
            st.warning(f"Revenue trend is declining by {abs(growth_value):.2f}%.")
        else:
            st.info("Revenue trend is stable.")