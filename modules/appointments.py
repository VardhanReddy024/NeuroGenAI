import streamlit as st
from database.db import (
    save_appointment,
    get_all_appointments,
    get_doctor_appointments,
    get_patient_appointments,
    update_appointment_status,
    get_doctor_profiles,
    update_doctor_availability,
    appointment_exists,
    save_patient_note,
    get_patient_history,
    get_doctor_notes,
    get_audit_logs
)

TIME_SLOTS = [
    "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "02:00 PM", "03:00 PM", "04:00 PM"
]

DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]


def status_text(status):
    if status == "Booked":
        return "🔵 Booked"
    if status == "Completed":
        return "🟢 Completed"
    if status == "Cancelled":
        return "🔴 Cancelled"
    return f"⚪ {status}"


def recommendation_from_issue(issue: str) -> str:
    issue = issue.lower().strip()

    mapping = {
        "Cardiology": ["chest", "heart", "bp", "blood pressure", "cardiac", "breath"],
        "Neurology": ["headache", "migraine", "brain", "nerve", "seizure", "stroke", "memory"],
        "Orthopedics": ["bone", "joint", "leg", "arm", "fracture", "back pain", "knee", "shoulder"],
        "General": ["fever", "cold", "cough", "infection", "stomach", "weakness"]
    }

    for spec, keywords in mapping.items():
        for word in keywords:
            if word in issue:
                return spec
    return "General"


def show_doctor_cards(doctor_df):
    st.subheader("👨‍⚕️ Available Doctors")

    if doctor_df.empty:
        st.info("No doctors found.")
        return

    cols = st.columns(3)
    for i, row in doctor_df.iterrows():
        days = row["availability_days"] if row["availability_days"] else "Not set"
        slots = row["availability_slots"] if row["availability_slots"] else "Not set"

        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <h4>Dr. {row['username']}</h4>
                <p><b>Specialization:</b> {row['specialization'] if row['specialization'] else 'General'}</p>
                <p><b>Status:</b> {row['doctor_status']}</p>
                <p><b>Days:</b> {days}</p>
                <p><b>Slots:</b> {slots}</p>
            </div>
            """, unsafe_allow_html=True)


def patient_booking_portal(patient_name, doctors):
    st.subheader("📅 Book Appointment")

    doctor_df = doctors.copy()
    if doctor_df.empty:
        st.warning("No doctors available.")
        return

    show_doctor_cards(doctor_df)
    st.markdown("---")

    issue = st.text_area("Describe Health Issue")
    recommended_spec = recommendation_from_issue(issue) if issue else None

    if recommended_spec:
        st.info(f"Recommended specialization based on issue: **{recommended_spec}**")

    specialization_options = ["All"] + sorted(doctor_df["specialization"].fillna("General").unique().tolist())
    default_index = specialization_options.index(recommended_spec) if recommended_spec in specialization_options else 0
    selected_spec = st.selectbox("Filter by Specialization", specialization_options, index=default_index)

    appointment_date = st.date_input("Appointment Date")
    selected_day_name = appointment_date.strftime("%A")

    filtered_doctors = doctor_df.copy()

    if selected_spec != "All":
        filtered_doctors = filtered_doctors[
            filtered_doctors["specialization"].fillna("General") == selected_spec
        ]

    if not filtered_doctors.empty:
        filtered_doctors = filtered_doctors[
            filtered_doctors["doctor_status"].fillna("Available") == "Available"
        ]

    if not filtered_doctors.empty:
        filtered_doctors = filtered_doctors[
            filtered_doctors["availability_days"].fillna("").apply(
                lambda x: selected_day_name in [d.strip() for d in x.split(",") if d.strip()]
                if x else False
            )
        ]

    if filtered_doctors.empty:
        st.warning("No doctors available for the selected specialization/day.")
        return

    doctor_names = filtered_doctors["username"].tolist()
    doctor_name = st.selectbox("Select Doctor", doctor_names)

    selected_doc_row = filtered_doctors[filtered_doctors["username"] == doctor_name].iloc[0]
    available_slots = [s.strip() for s in str(selected_doc_row["availability_slots"]).split(",") if s.strip()]
    if not available_slots:
        available_slots = TIME_SLOTS

    appointment_time = st.selectbox("Time Slot", available_slots)

    if st.button("Book Appointment"):
        if not issue.strip():
            st.warning("Please describe your issue.")
            return

        if appointment_exists(doctor_name, str(appointment_date), appointment_time):
            st.error("This slot is already booked. Choose another slot.")
            return

        save_appointment(
            patient_name,
            doctor_name,
            str(appointment_date),
            appointment_time,
            issue,
            "Booked"
        )
        st.success(f"Appointment booked with Dr. {doctor_name} on {appointment_date} at {appointment_time}")

    st.subheader("🧾 My Appointments")
    patient_df = get_patient_appointments(patient_name)

    if patient_df.empty:
        st.info("No appointments yet.")
    else:
        status_filter = st.selectbox("Filter My Appointments by Status", ["All", "Booked", "Completed", "Cancelled"])
        if status_filter != "All":
            patient_df = patient_df[patient_df["status"] == status_filter]

        for _, row in patient_df.iterrows():
            st.markdown(f"""
            <div class="card">
                <b>Doctor:</b> Dr. {row['doctor_name']} <br>
                <b>Date:</b> {row['appointment_date']} <br>
                <b>Time:</b> {row['appointment_time']} <br>
                <b>Issue:</b> {row['issue']} <br>
                <b>Status:</b> {status_text(row['status'])}
            </div>
            """, unsafe_allow_html=True)

    st.subheader("📂 My Medical History")
    history_df = get_patient_history(patient_name)
    if history_df.empty:
        st.info("No medical history available yet.")
    else:
        st.dataframe(history_df, use_container_width=True)


def doctor_panel(doctor_name):
    st.subheader(f"🩺 Doctor Panel - Dr. {doctor_name}")

    st.markdown("### 🗓 Manage Availability")
    doctor_profiles = get_doctor_profiles()
    doctor_row = doctor_profiles[doctor_profiles["username"] == doctor_name]

    current_days = []
    current_slots = []
    current_status = "Available"

    if not doctor_row.empty:
        row = doctor_row.iloc[0]
        current_days = [d.strip() for d in str(row["availability_days"]).split(",") if d.strip()]
        current_slots = [s.strip() for s in str(row["availability_slots"]).split(",") if s.strip()]
        current_status = row["doctor_status"] if row["doctor_status"] else "Available"

    selected_days = st.multiselect("Available Days", DAY_NAMES, default=current_days)
    selected_slots = st.multiselect("Available Slots", TIME_SLOTS, default=current_slots)
    selected_status = st.selectbox(
        "Doctor Status",
        ["Available", "Busy", "On Leave"],
        index=["Available", "Busy", "On Leave"].index(current_status)
        if current_status in ["Available", "Busy", "On Leave"] else 0
    )

    if st.button("Save Availability"):
        update_doctor_availability(doctor_name, selected_days, selected_slots, selected_status)
        st.success("Availability updated successfully.")
        st.rerun()

    st.markdown("---")
    st.subheader("📋 Assigned Appointments")
    df = get_doctor_appointments(doctor_name)

    if df.empty:
        st.info("No appointments assigned.")
    else:
        search_patient = st.text_input("Search Patient Name")
        status_filter = st.selectbox("Filter by Status", ["All", "Booked", "Completed", "Cancelled"], key="doctor_status_filter")

        if search_patient:
            df = df[df["patient_name"].str.contains(search_patient, case=False, na=False)]
        if status_filter != "All":
            df = df[df["status"] == status_filter]

        for _, row in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <b>Appointment ID:</b> {row['id']} <br>
                <b>Patient:</b> {row['patient_name']} <br>
                <b>Date:</b> {row['appointment_date']} <br>
                <b>Time:</b> {row['appointment_time']} <br>
                <b>Issue:</b> {row['issue']} <br>
                <b>Status:</b> {status_text(row['status'])}
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Update Appointment Status")
        selected_id = st.selectbox("Appointment ID", df["id"].tolist())
        new_status = st.selectbox("New Status", ["Booked", "Completed", "Cancelled"])

        if st.button("Update Status"):
            update_appointment_status(selected_id, new_status, actor=doctor_name)
            st.success("Appointment updated.")
            st.rerun()

    st.markdown("---")
    st.subheader("📝 Add Patient Notes / History")
    patient_name = st.text_input("Patient Name")
    diagnosis = st.text_input("Diagnosis")
    prescription = st.text_area("Prescription")
    follow_up_date = st.date_input("Follow-up Date", key="follow_up")
    notes = st.text_area("Doctor Notes")

    if st.button("Save Patient Notes"):
        if not patient_name.strip():
            st.warning("Enter patient name.")
        else:
            save_patient_note(
                patient_name=patient_name,
                doctor_name=doctor_name,
                diagnosis=diagnosis,
                prescription=prescription,
                follow_up_date=str(follow_up_date),
                notes=notes
            )
            st.success("Patient notes saved.")

    st.subheader("📚 My Saved Notes")
    notes_df = get_doctor_notes(doctor_name)
    if notes_df.empty:
        st.info("No notes available.")
    else:
        st.dataframe(notes_df, use_container_width=True)


def admin_appointment_panel():
    st.subheader("📋 All Appointments")

    df = get_all_appointments()
    if df.empty:
        st.info("No appointments found.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        search_patient = st.text_input("Search Patient")
    with col2:
        search_doctor = st.text_input("Search Doctor")
    with col3:
        status_filter = st.selectbox("Status Filter", ["All", "Booked", "Completed", "Cancelled"])

    filtered_df = df.copy()

    if search_patient:
        filtered_df = filtered_df[filtered_df["patient_name"].str.contains(search_patient, case=False, na=False)]
    if search_doctor:
        filtered_df = filtered_df[filtered_df["doctor_name"].str.contains(search_doctor, case=False, na=False)]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div class="card">
            <b>Appointment ID:</b> {row['id']} <br>
            <b>Patient:</b> {row['patient_name']} <br>
            <b>Doctor:</b> Dr. {row['doctor_name']} <br>
            <b>Date:</b> {row['appointment_date']} <br>
            <b>Time:</b> {row['appointment_time']} <br>
            <b>Issue:</b> {row['issue']} <br>
            <b>Status:</b> {status_text(row['status'])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Admin Control")
    selected_id = st.selectbox("Appointment ID", filtered_df["id"].tolist())
    new_status = st.selectbox("Update Status", ["Booked", "Completed", "Cancelled"], key="admin_status")

    if st.button("Update"):
        update_appointment_status(selected_id, new_status, actor="Admin")
        st.success("Status updated.")
        st.rerun()

    st.markdown("---")
    st.subheader("🧾 Audit Log")
    logs_df = get_audit_logs()
    if logs_df.empty:
        st.info("No audit logs yet.")
    else:
        st.dataframe(logs_df, use_container_width=True)


def admin_home_services_and_queries_panel():
    st.subheader("🏡 Home Care Service Bookings")
    from database.db import get_home_services, update_home_service_status
    hs_df = get_home_services()
    if hs_df.empty:
        st.info("No home service requests found.")
    else:
        st.dataframe(hs_df, use_container_width=True)
        
        st.markdown("### Update Home Service Status")
        h_cols = st.columns([1, 1, 1])
        with h_cols[0]:
            sel_hs_id = st.selectbox("Select Home Service Request ID", hs_df["id"].tolist())
        with h_cols[1]:
            new_hs_status = st.selectbox("Select Status", ["Pending", "Scheduled", "Completed", "Cancelled"], key="hs_status_update_sel")
        with h_cols[2]:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Update Home Service Status", key="hs_status_update_btn"):
                update_home_service_status(sel_hs_id, new_hs_status)
                st.success(f"Home Service #{sel_hs_id} status updated to {new_hs_status}!")
                st.rerun()

    st.markdown("---")
    st.subheader("✉️ Received Contact Queries")
    from database.db import get_contact_queries
    queries_df = get_contact_queries()
    if queries_df.empty:
        st.info("No contact inquiries found.")
    else:
        st.dataframe(queries_df, use_container_width=True)