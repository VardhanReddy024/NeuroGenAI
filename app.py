import streamlit as st
import pandas as pd

from database.db import init_db, load_data, get_doctor_profiles, get_all_appointments
from modules.auth import login, signup, logout
from modules.data_loader import preprocess
from modules.filters import apply_filters
from modules.ui_helpers import kpi_card
from modules.charts import show_charts

from modules.insights import show_insights
from modules.ml_model import predict, predict_appointments
from modules.appointments import (
    patient_booking_portal,
    doctor_panel,
    admin_appointment_panel,
    admin_home_services_and_queries_panel
)
from modules.website_features import show_home, show_about, show_services, show_contact

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="NeuroGen AI - Hospital Dashboard", layout="wide")

# ---------- PREMIUM CSS ----------
import pathlib
css_path = pathlib.Path(__file__).parent / "static" / "style.css"
if css_path.is_file():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "login"

# ---------- RESET CSS FOR NON-LOGIN PAGES ----------
def inject_reset_css():
    st.markdown("""
    <style>
    [data-testid="stHeader"] {
        display: flex !important;
    }
    [data-testid="stAppViewContainer"] {
        background-image: none !important;
    }
    [data-testid="stMainBlockContainer"] {
        background-color: transparent !important;
        border-radius: 0px !important;
        padding: 6rem 5rem 2rem !important;
        max-width: 100% !important;
        box-shadow: none !important;
        margin: 0 auto !important;
        border: none !important;
    }
    div[data-testid="stTextInput"] label, div[data-testid="stTextArea"] label {
        display: block !important;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: rgba(5, 12, 24, 0.6) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        background-image: none !important;
    }
    div[data-testid="stSelectbox"] label {
        color: #F8FAFC !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        display: block !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: rgba(5, 12, 24, 0.6) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 10px rgba(0, 180, 216, 0.5));">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#grad1)"/>
        <path d="M2 17L12 22L22 17" stroke="#00E5A8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 12L12 17L22 12" stroke="#00B4D8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <defs>
            <linearGradient id="grad1" x1="2" y1="2" x2="22" y2="12" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#00B4D8" />
                <stop offset="100%" stop-color="#BD00FF" />
            </linearGradient>
        </defs>
    </svg>
    <div style="color: #FFFFFF; font-size: 24px; font-weight: 900; letter-spacing: -1px; margin-top: 8px; font-family: 'Outfit', sans-serif;">NeuroGen<span style="background: linear-gradient(135deg, #00B4D8, #00E5A8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"> AI</span></div>
    <div style="color: #64748B; font-size: 9px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-top: -2px;">HealthOS & MedX</div>
</div>
""", unsafe_allow_html=True)

nav_options = ["🏠 Home", "📖 About Us", "🛠️ Services", "📞 Contact Us"]
portal_label = "🏥 Patient & Staff Portal" if st.session_state["logged_in"] else "🔐 Log In / Register"
nav_options.append(portal_label)

selected_page = st.sidebar.radio("Navigation Menu", nav_options, label_visibility="collapsed")

if selected_page == "🏠 Home":
    inject_reset_css()
    show_home()
elif selected_page == "📖 About Us":
    inject_reset_css()
    show_about()
elif selected_page == "🛠️ Services":
    inject_reset_css()
    show_services()
elif selected_page == "📞 Contact Us":
    inject_reset_css()
    show_contact()
else:
    # ---------- PORTAL / LOGIN FLOW ----------
    if not st.session_state["logged_in"]:
        # Cache base64 background image
        if "bg_base64" not in st.session_state:
            import base64
            try:
                with open("aiimage.png", "rb") as f:
                    st.session_state["bg_base64"] = base64.b64encode(f.read()).decode()
            except Exception:
                st.session_state["bg_base64"] = ""
        bg_base64 = st.session_state["bg_base64"]
        
        # Inject CSS
        original_css = """
        div[data-testid="stTextInput"] input {
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            padding: 12px 16px 12px 42px !important;
            font-size: 15px !important;
            font-weight: 500 !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #00B4D8 !important;
            box-shadow: 0 0 0 3px rgba(0, 180, 216, 0.15) !important;
        }
        div[key="login_user"] input, div[key="signup_user"] input {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394A3B8' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: 14px center !important;
            background-size: 20px !important;
        }
        div[key="login_pass"] input, div[key="signup_pass"] input {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394A3B8' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: 14px center !important;
            background-size: 20px !important;
        }
        div[data-testid="stSelectbox"] label {
            color: #475569 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            margin-bottom: 4px !important;
            display: block !important;
        }
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
        }
        div[data-testid="stCheckbox"] label p {
            color: #64748B !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }
        .forgot-pass-link {
            color: #00B4D8 !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            text-decoration: none !important;
        }
        .forgot-pass-link:hover {
            color: #00B4D8 !important;
            text-decoration: none !important;
        }
        div.stButton > button[data-testid="stBaseButton-primary"] {
            background-color: #00B4D8 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            width: 100% !important;
            text-transform: uppercase !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 180, 216, 0.2), 0 2px 4px -1px rgba(0, 180, 216, 0.1) !important;
            margin-top: 15px !important;
        }
        div.stButton > button[data-testid="stBaseButton-primary"]:hover {
            background-color: #0096B1 !important;
            box-shadow: 0 10px 15px -3px rgba(0, 180, 216, 0.3), 0 4px 6px -2px rgba(0, 180, 216, 0.15) !important;
            transform: translateY(-1px) !important;
        }
        div.stButton > button[data-testid="stBaseButton-secondary"] {
            background-color: transparent !important;
            color: #00B4D8 !important;
            border: 1.5px solid #00B4D8 !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            width: 100% !important;
            text-transform: uppercase !important;
            transition: all 0.2s ease !important;
            margin-top: 8px !important;
        }
        div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
            background-color: rgba(0, 180, 216, 0.08) !important;
            color: #0096B1 !important;
            border-color: #0096B1 !important;
        }
        .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
            text-align: center;
        }
        .logo-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 2px;
        }
        .logo-icon {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .logo-text {
            font-size: 30px;
            font-weight: 800;
            color: #0F172A;
            letter-spacing: -0.5px;
        }
        .logo-text span {
            color: #F8FAFC;
        }
        .logo-subtext {
            font-size: 10px;
            font-weight: 700;
            color: #64748B;
            letter-spacing: 5px;
            text-transform: uppercase;
            margin-top: -2px;
            margin-bottom: 14px;
        }
        .logo-tagline {
            font-size: 14px;
            color: #64748B;
            font-weight: 500;
            margin-bottom: 20px;
        }
        """

        # Build CSS using concatenation to avoid f-string brace issues
        if bg_base64:
            bg_style = 'background-image: linear-gradient(rgba(15, 23, 42, 0.15), rgba(15, 23, 42, 0.15)), url("data:image/png;base64,' + bg_base64 + '");'
        else:
            bg_style = 'background-image: linear-gradient(135deg, #0F172A 0%, #1E293B 40%, #0E4D64 70%, #00B4D8 100%);'

        css = (
            "<style>"
            + '[data-testid="stHeader"] { display: none !important; } '
            + 'footer { display: none !important; } '
            + '[data-testid="stAppViewContainer"] { '
            + bg_style
            + ' background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; } '
            + '[data-testid="stMainBlockContainer"] { '
            + 'background-color: #FFFFFF !important; border-radius: 20px !important; padding: 45px 50px !important; '
            + 'max-width: 460px !important; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important; '
            + 'margin: auto !important; margin-top: 8vh !important; margin-bottom: 8vh !important; '
            + 'border: 1px solid rgba(255, 255, 255, 0.8) !important; } '
            + original_css
            + "</style>"
        )
        st.markdown(css, unsafe_allow_html=True)

        if st.session_state["auth_mode"] == "login":
            if login():
                st.rerun()
        else:
            signup()
    else:
        # ---------- AFTER LOGIN PORTAL ----------
        inject_reset_css()
        # Mobile mode toggle
        mobile_mode = st.sidebar.toggle("📱 Mobile Mode", value=False)
        # If mobile mode, hide sidebar and show top navigation bar
        if mobile_mode:
            # Mobile top navigation bar
            nav_cols = st.columns(len(nav_options))
            for col, option in zip(nav_cols, nav_options):
                if col.button(option, key=f"mobile_nav_{option}"):
                    selected_page = option
                    st.experimental_rerun()
        else:
            st.sidebar.markdown("### ☰ Staff & Patient Menu")
        st.sidebar.success(f"User: {st.session_state['username']}")
        st.sidebar.info(f"Role: {st.session_state['role']}")
        logout()

        # ---------- HEADER ----------
        st.markdown('<div class="hero-title">🏥 NeuroGen AI Management Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Analytics • Appointments • AI • Healthcare</div>', unsafe_allow_html=True)

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
                # Mobile layout: three rows with two columns each
                rows = [st.columns(2) for _ in range(3)]
                labels = ["Total Patients", "Total Revenue", "Total Expense",
                          "Total Doctors", "Appointments", "Avg Patient Stay"]
                values = [f"{total_patients:,}",
                          f"₹{total_revenue:,.0f}",
                          f"₹{total_expense:,.0f}",
                          f"{total_doctors:,}",
                          f"{total_appointments:,}",
                          f"{0 if pd.isna(avg_stay) else round(avg_stay,1)} Days"]
                for i, (col1, col2) in enumerate(rows):
                    with col1:
                        st.markdown(kpi_card(labels[i*2], values[i*2]), unsafe_allow_html=True)
                    with col2:
                        st.markdown(kpi_card(labels[i*2+1], values[i*2+1]), unsafe_allow_html=True)
            else:
                # Desktop layout: single row with six columns
                cols = st.columns(6)
                labels = ["Total Patients", "Total Revenue", "Total Expense",
                          "Total Doctors", "Appointments", "Avg Patient Stay"]
                values = [f"{total_patients:,}",
                          f"₹{total_revenue:,.0f}",
                          f"₹{total_expense:,.0f}",
                          f"{total_doctors:,}",
                          f"{total_appointments:,}",
                          f"{0 if pd.isna(avg_stay) else round(avg_stay,1)} Days"]
                for col, label, value in zip(cols, labels, values):
                    with col:
                        st.markdown(kpi_card(label, value), unsafe_allow_html=True)

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

            st.markdown('<div class="section-title">🏡 Doorstep Home Services & Patient Inquiries</div>', unsafe_allow_html=True)
            admin_home_services_and_queries_panel()

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

            # My doorstep home services
            st.markdown('---')
            st.markdown('<div class="section-title">🏡 My Home Service Doorstep Visits</div>', unsafe_allow_html=True)
            from database.db import get_home_services
            my_hs_df = get_home_services(patient_name=username)
            if my_hs_df.empty:
                st.info("You haven't requested any doorstep home services yet. Go to the 'Services' tab to book one!")
            else:
                st.dataframe(my_hs_df, use_container_width=True)

        # ---------- FALLBACK ----------
        else:
            st.error("Invalid role")