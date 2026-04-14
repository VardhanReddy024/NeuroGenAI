import streamlit as st

def show_kpis(df):
    total_patients = df['Patient_ID'].nunique()
    total_revenue = df['Revenue'].sum()
    total_expense = df['Expense'].sum()
    avg_los = df['Length_of_Stay'].mean()

    def card(title, value):
        return f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(card("Patients", total_patients), unsafe_allow_html=True)
    col2.markdown(card("Revenue", f"₹{total_revenue:,.0f}"), unsafe_allow_html=True)
    col3.markdown(card("Expense", f"₹{total_expense:,.0f}"), unsafe_allow_html=True)
    col4.markdown(card("Avg Stay", f"{avg_los:.2f} days"), unsafe_allow_html=True)