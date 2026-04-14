import streamlit as st
import pandas as pd

from database.db import init_db, load_data, get_doctor_profiles, get_all_appointments
from modules.auth import login, signup, logout
from modules.data_loader import preprocess
from modules.filters import apply_filters
from modules.charts import show_charts
from modules.insights import show_insights
from modules.ml_model import predict, predict_appointments
from modules.appointments import (
    patient_booking_portal,
    doctor_panel,
    admin_appointment_panel
)

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Hospital Dashboard", layout="wide")

# ---------- INIT ----------
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state["db_initialized"] = True

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

# ---------- SIDEBAR ----------
st.sidebar.markdown("### ☰ Menu")
menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])
mobile_mode = st.sidebar.toggle("📱 Mobile Mode", value=False)

# ---------- PREMIUM CSS ----------
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #020617, #081018, #0f172a);
    color: #F8FAFC;
}}

.hero-title {{
    text-align: center;
    font-size: 60px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 0 40px rgba(0,229,168,0.8);
    margin-top: 30px;
}}

.hero-sub {{
    text-align: center;
    font-size: 18px;
    color: #94A3B8;
    margin-bottom: 25px;
}}

.banner-img img {{
    width: 100%;
    height: 420px;
    object-fit: cover;
    border-radius: 20px;
    box-shadow: 0 0 50px rgba(0,229,168,0.25);
}}

section[data-testid="stSidebar"] {{
    background: #020617;
}}

.kpi-box {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,229,168,0.15);
    border-radius: 16px;
    padding: 12px;
    text-align: center;
}}

@media (max-width: 768px) {{
    .hero-title {{
        font-size: 32px !important;
        margin-top: 10px !important;
    }}

    .hero-sub {{
        font-size: 14px !important;
        margin-bottom: 14px !important;
    }}

    .banner-img img {{
        height: 220px !important;
        border-radius: 14px !important;
    }}

    .block-container {{
        padding-top: 0.8rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }}
}}

{" .hero-title { font-size: 34px !important; margin-top: 10px !important; } .hero-sub { font-size: 14px !important; } .banner-img img { height: 220px !important; } .block-container { padding-top: 0.8rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; } " if mobile_mode else ""}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="hero-title">🏥 Hospital Management Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Analytics • Appointments • AI • Healthcare</div>', unsafe_allow_html=True)

# ---------- BEFORE LOGIN ----------
if not st.session_state["logged_in"]:
    st.markdown('<div class="banner-img">', unsafe_allow_html=True)
    st.image("aiimage.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if menu == "Login":
        if login():
            st.rerun()
    else:
        signup()

    st.stop()

# ---------- AFTER LOGIN ----------
st.sidebar.success(f"User: {st.session_state['username']}")
st.sidebar.info(f"Role: {st.session_state['role']}")
logout()

# ---------- LOAD DATA ----------
df = preprocess(load_data())
doctor_profiles = get_doctor_profiles()
appointments_df = get_all_appointments()

role = st.session_state["role"]
username = st.session_state["username"]

# ---------- KPI SECTION ----------
st.markdown("### 🔍 Overview")

total_revenue = df["Revenue"].sum()
total_expense = df["Expense"].sum()
total_profit = total_revenue - total_expense

if mobile_mode:
    r1c1, r1c2 = st.columns(2)
    r2c1, r2c2 = st.columns(2)

    with r1c1:
        st.metric("Appointments", len(appointments_df))
    with r1c2:
        st.metric("Doctors", len(doctor_profiles))
    with r2c1:
        st.metric("Patients", df["Patient_ID"].nunique())
    with r2c2:
        st.metric("Profit", f"₹{total_profit:,.0f}")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Appointments", len(appointments_df))
    c2.metric("Doctors", len(doctor_profiles))
    c3.metric("Patients", df["Patient_ID"].nunique())
    c4.metric("Profit", f"₹{total_profit:,.0f}")

# ---------- ADMIN ----------
if role == "Admin":
    filtered_df = apply_filters(df)

    if filtered_df.empty:
        st.warning("No data available")
        st.stop()

    st.markdown("### 📊 Dashboard")
    show_charts(filtered_df)

    st.markdown("### 📌 Insights")
    show_insights(filtered_df)

    st.markdown("### 📄 Data Table")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", csv, "hospital_data.csv")

    st.markdown("### 📅 Appointment Management")
    admin_appointment_panel()

    st.markdown("### 🤖 Predictions")
    temp = filtered_df.copy()
    temp["Month"] = temp["Admission_Date"].dt.to_period("M").astype(str)
    temp = temp.groupby("Month")["Revenue"].sum().reset_index()

    predict(temp)
    predict_appointments()

# ---------- DOCTOR ----------
elif role == "Doctor":
    st.markdown(f"### 🩺 Doctor Panel - {username}")
    doctor_panel(username)

# ---------- PATIENT ----------
elif role == "Patient":
    st.markdown(f"### 👤 Patient Portal - {username}")
    patient_booking_portal(username, doctor_profiles)

# ---------- FALLBACK ----------
else:
    st.error("Invalid role")