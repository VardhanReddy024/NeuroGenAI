import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db import get_all_appointments


def _apply_dark_style(fig, height=320):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", size=13),
        title=dict(font=dict(color="#F8FAFC", size=18)),
        xaxis=dict(
            title_font=dict(color="#E2E8F0"),
            tickfont=dict(color="#CBD5E1"),
            gridcolor="rgba(255,255,255,0.10)"
        ),
        yaxis=dict(
            title_font=dict(color="#E2E8F0"),
            tickfont=dict(color="#CBD5E1"),
            gridcolor="rgba(255,255,255,0.10)"
        ),
        legend=dict(font=dict(color="#E2E8F0")),
        margin=dict(l=40, r=20, t=55, b=40)
    )
    return fig


def show_charts(df):
    if df.empty:
        st.warning("No data available for charts.")
        return pd.DataFrame()

    chart_df = df.copy()
    chart_df["Month"] = chart_df["Admission_Date"].dt.to_period("M").astype(str)

    if "Profit" not in chart_df.columns:
        chart_df["Profit"] = chart_df["Revenue"] - chart_df["Expense"]

    monthly_df = chart_df.groupby("Month")[["Revenue", "Expense", "Profit"]].sum().reset_index()
    dept_df = chart_df.groupby("Department")[["Revenue", "Expense", "Profit"]].sum().reset_index()
    patient_count_df = chart_df["Department"].value_counts().reset_index()
    patient_count_df.columns = ["Department", "Patients"]

    c1, c2 = st.columns(2, gap="large")

    with c1:
        fig = px.line(monthly_df, x="Month", y="Revenue", markers=True, title="Revenue Trend")
        fig.update_traces(line=dict(width=3))
        st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    with c2:
        fig = px.pie(patient_count_df, names="Department", values="Patients", hole=0.50, title="Department Patient Share")
        st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    c3, c4 = st.columns(2, gap="large")

    with c3:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=dept_df["Department"], y=dept_df["Revenue"], name="Revenue"))
        fig.add_trace(go.Bar(x=dept_df["Department"], y=dept_df["Expense"], name="Expense"))
        fig.update_layout(barmode="group", title="Revenue vs Expense by Department")
        st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    with c4:
        fig = px.area(monthly_df, x="Month", y=["Revenue", "Expense", "Profit"], title="Monthly Financial Trend")
        st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    c5, c6 = st.columns(2, gap="large")

    with c5:
        if "Doctor_Name" in chart_df.columns:
            doctor_rev = chart_df.groupby("Doctor_Name")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
            fig = px.bar(doctor_rev, x="Doctor_Name", y="Revenue", title="Revenue by Doctor")
            st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    with c6:
        if "Doctor_Name" in chart_df.columns:
            doctor_patients = chart_df.groupby("Doctor_Name")["Patient_ID"].count().reset_index(name="Patients")
            doctor_patients = doctor_patients.sort_values("Patients", ascending=False)
            fig = px.bar(doctor_patients, x="Doctor_Name", y="Patients", title="Patients by Doctor")
            st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    c7, c8 = st.columns(2, gap="large")

    with c7:
        if "Gender" in chart_df.columns:
            gender_df = chart_df["Gender"].value_counts().reset_index()
            gender_df.columns = ["Gender", "Count"]
            fig = px.pie(gender_df, names="Gender", values="Count", hole=0.55, title="Gender Distribution")
            st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    with c8:
        if "Payment_Mode" in chart_df.columns:
            pay_df = chart_df["Payment_Mode"].value_counts().reset_index()
            pay_df.columns = ["Payment_Mode", "Count"]
            fig = px.bar(pay_df, x="Payment_Mode", y="Count", title="Payment Mode Distribution")
            st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    c9, c10 = st.columns(2, gap="large")

    with c9:
        if "Age" in chart_df.columns:
            fig = px.histogram(chart_df, x="Age", nbins=20, title="Age Distribution")
            st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    with c10:
        fig = px.bar(
            dept_df.sort_values("Profit", ascending=False),
            x="Department",
            y="Profit",
            title="Profit by Department"
        )
        st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    appointments_df = get_all_appointments()

    if not appointments_df.empty:
        c11, c12 = st.columns(2, gap="large")

        with c11:
            doctor_counts = appointments_df["doctor_name"].value_counts().reset_index()
            doctor_counts.columns = ["Doctor", "Appointments"]
            fig = px.bar(doctor_counts, x="Doctor", y="Appointments", title="Appointments by Doctor")
            st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

        with c12:
            status_counts = appointments_df.groupby(["doctor_name", "status"]).size().reset_index(name="Count")
            fig = px.bar(status_counts, x="doctor_name", y="Count", color="status", title="Doctor-wise Appointment Status")
            st.plotly_chart(_apply_dark_style(fig, 300), use_container_width=True)

    return monthly_df