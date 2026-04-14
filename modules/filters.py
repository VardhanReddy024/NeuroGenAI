import streamlit as st
import pandas as pd

def apply_filters(df):
    st.sidebar.header("Filters")

    departments = st.sidebar.multiselect(
        "Department",
        options=sorted(df["Department"].dropna().unique().tolist()),
        default=sorted(df["Department"].dropna().unique().tolist())
    )

    doctors = st.sidebar.multiselect(
        "Doctor",
        options=sorted(df["Doctor_Name"].dropna().unique().tolist()) if "Doctor_Name" in df.columns else [],
        default=sorted(df["Doctor_Name"].dropna().unique().tolist()) if "Doctor_Name" in df.columns else []
    )

    genders = st.sidebar.multiselect(
        "Gender",
        options=sorted(df["Gender"].dropna().unique().tolist()) if "Gender" in df.columns else [],
        default=sorted(df["Gender"].dropna().unique().tolist()) if "Gender" in df.columns else []
    )

    payment_modes = st.sidebar.multiselect(
        "Payment Mode",
        options=sorted(df["Payment_Mode"].dropna().unique().tolist()) if "Payment_Mode" in df.columns else [],
        default=sorted(df["Payment_Mode"].dropna().unique().tolist()) if "Payment_Mode" in df.columns else []
    )

    min_age = int(df["Age"].min()) if "Age" in df.columns else 0
    max_age = int(df["Age"].max()) if "Age" in df.columns else 100
    age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

    date_range = st.sidebar.date_input(
        "Admission Date Range",
        value=(df["Admission_Date"].min(), df["Admission_Date"].max())
    )

    if not departments:
        return df.iloc[0:0]
    if "Doctor_Name" in df.columns and not doctors:
        return df.iloc[0:0]
    if "Gender" in df.columns and not genders:
        return df.iloc[0:0]
    if "Payment_Mode" in df.columns and not payment_modes:
        return df.iloc[0:0]

    if isinstance(date_range, (tuple, list)):
        if len(date_range) != 2:
            return df.iloc[0:0]
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
    else:
        start_date = pd.to_datetime(date_range)
        end_date = pd.to_datetime(date_range)

    filtered_df = df.copy()

    filtered_df = filtered_df[
        (filtered_df["Department"].isin(departments)) &
        (filtered_df["Admission_Date"] >= start_date) &
        (filtered_df["Admission_Date"] <= end_date)
    ]

    if "Doctor_Name" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Doctor_Name"].isin(doctors)]

    if "Gender" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Gender"].isin(genders)]

    if "Payment_Mode" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Payment_Mode"].isin(payment_modes)]

    if "Age" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["Age"].between(age_range[0], age_range[1])
        ]

    return filtered_df