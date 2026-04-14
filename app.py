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

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #081018, #0f172a);
    color: #F8FAFC;
}

/* TITLE */
.hero-title {
    text-align: center;
    font-size: 58px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 0 35px rgba(0,229,168,0.65);
    margin-top: 22px;
    margin-bottom: 4px;
}

.hero-sub {
    text-align: center;
    font-size: 18px;
    color: #94A3B8;
    margin-bottom: 20px;
}

/* IMAGE */
.banner-img img {
    width: 100%;
    height: 420px;
    object-fit: cover;
    border-radius: 20px;
    box-shadow: 0 0 40px rgba(0,229,168,0.20);
    margin-bottom: 8px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* KPI CARDS */
.kpi-wrapper {
    margin-top: 8px;
    margin-bottom: 20px;
}

.kpi-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(0,229,168,0.18);
    border-radius: 18px;
    padding: 18px 14px;
    text-align: center;
    box-shadow: 0 0 18px rgba(0,229,168,0.08);
    min-height: 120px;
}

.kpi-label {
    color: #CBD5E1;
    font-size: 14px;
    margin-bottom: 10px;
    font-weight: 600;
}

.kpi-value {
    color: #F8FAFC;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.1;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: 8px;
    margin-bottom: 12px;
}

/* DATAFRAME / BUTTONS */
div.stDownloadButton > button {
    background-color: #111 !important;
    color: white !important;
    border-radius: 10px;
    border: 1px solid #00E5A8;
}

/* MOBILE */
@media (max-width: 768px) {
    .hero-title {
        font-size: 34px !important;
        margin-top: 10px !important;
    }

    .hero-sub {
        font-size: 14px !important;
        margin-bottom: 14px !important;
    }

    .banner-img img {
        height: 220px !important;
        border-radius: 14px !important;
    }

    .kpi-value {
        font-size: 26px !important;
    }

    .block-container {
        padding-top: 0.8rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

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

# ---------- ADMIN ----------
if role == "Admin":
    filtered_df = apply_filters(df)

    if filtered_df.empty:
        st.warning("No data available")
        st.stop()

    total_patients = filtered_df["Patient_ID"].nunique() if "Patient_ID" in filtered_df.columns else len(filtered_df)
    total_revenue = filtered_df["Revenue"].sum() if "Revenue" in filtered_df.columns else 0
    total_expense = filtered_df["Expense"].sum() if "Expense" in filtered_df.columns else 0
    total_doctors = filtered_df["Doctor_Name"].nunique() if "Doctor_Name" in filtered_df.columns else len(doctor_profiles)
    total_appointments = len(appointments_df)

    if "Length_of_Stay" in filtered_df.columns:
        avg_stay = filtered_df["Length_of_Stay"].mean()
    elif {"Admission_Date", "Discharge_Date"}.issubset(filtered_df.columns):
        avg_stay = (filtered_df["Discharge_Date"] - filtered_df["Admission_Date"]).dt.days.mean()
    else:
        avg_stay = 0

    # ---------- HIGHLIGHT KPI CARDS ----------
    st.markdown('<div class="section-title">📌 Overview</div>', unsafe_allow_html=True)

    if mobile_mode:
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)

        with row1_col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Patients</div>
                <div class="kpi-value">{total_patients:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with row1_col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">₹{total_revenue:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with row2_col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Expense</div>
                <div class="kpi-value">₹{total_expense:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with row2_col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Doctors</div>
                <div class="kpi-value">{total_doctors:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with row3_col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Appointments</div>
                <div class="kpi-value">{total_appointments:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with row3_col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Avg Patient Stay</div>
                <div class="kpi-value">{0 if pd.isna(avg_stay) else round(avg_stay, 1)} Days</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        c1, c2, c3, c4, c5, c6 = st.columns(6)

        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Patients</div>
                <div class="kpi-value">{total_patients:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">₹{total_revenue:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Expense</div>
                <div class="kpi-value">₹{total_expense:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Doctors</div>
                <div class="kpi-value">{total_doctors:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with c5:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Appointments</div>
                <div class="kpi-value">{total_appointments:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with c6:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Avg Patient Stay</div>
                <div class="kpi-value">{0 if pd.isna(avg_stay) else round(avg_stay, 1)} Days</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------- DASHBOARD ----------
    st.markdown('<div class="section-title">📊 Dashboard</div>', unsafe_allow_html=True)
    show_charts(filtered_df)

    st.markdown('<div class="section-title">📌 Insights</div>', unsafe_allow_html=True)
    show_insights(filtered_df)

    st.markdown('<div class="section-title">📄 Data Table</div>', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", csv, "hospital_data.csv")

    st.markdown('<div class="section-title">📅 Appointment Management</div>', unsafe_allow_html=True)
    admin_appointment_panel()

    st.markdown('<div class="section-title">🤖 Predictions</div>', unsafe_allow_html=True)
    temp = filtered_df.copy()
    temp["Month"] = temp["Admission_Date"].dt.to_period("M").astype(str)
    temp = temp.groupby("Month")["Revenue"].sum().reset_index()

    predict(temp)
    predict_appointments()

# ---------- DOCTOR ----------
elif role == "Doctor":
    st.markdown(f'<div class="section-title">🩺 Doctor Panel - {username}</div>', unsafe_allow_html=True)
    doctor_panel(username)

# ---------- PATIENT ----------
elif role == "Patient":
    st.markdown(f'<div class="section-title">👤 Patient Portal - {username}</div>', unsafe_allow_html=True)
    patient_booking_portal(username, doctor_profiles)

# ---------- FALLBACK ----------
else:
    st.error("Invalid role")