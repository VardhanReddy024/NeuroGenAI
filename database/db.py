import pandas as pd
import sqlite3
from datetime import datetime

DB_NAME = "hospital.db"


# ---------- CONNECTION ----------
def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------- INIT DATABASE ----------
def init_db():
    conn = get_connection()

    # ---------- HOSPITAL TABLE ----------
    df = pd.read_csv("data/hospital_data.csv")
    df.to_sql("hospital", conn, if_exists="replace", index=False)

    # ---------- USERS TABLE ----------
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password BLOB,
        role TEXT,
        specialization TEXT,
        availability_days TEXT DEFAULT '',
        availability_slots TEXT DEFAULT '',
        doctor_status TEXT DEFAULT 'Available'
    )
    """)

    # ---------- APPOINTMENTS TABLE ----------
    conn.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        doctor_name TEXT,
        appointment_date TEXT,
        appointment_time TEXT,
        issue TEXT,
        status TEXT
    )
    """)

    # ---------- PATIENT HISTORY ----------
    conn.execute("""
    CREATE TABLE IF NOT EXISTS patient_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        doctor_name TEXT,
        diagnosis TEXT,
        prescription TEXT,
        follow_up_date TEXT,
        notes TEXT,
        created_at TEXT
    )
    """)

    # ---------- AUDIT LOG ----------
    conn.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        actor TEXT,
        action TEXT,
        old_status TEXT,
        new_status TEXT,
        log_time TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------- LOAD HOSPITAL DATA ----------
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM hospital", conn)
    conn.close()
    return df


# ---------- USERS ----------
def save_user(username, password, role, specialization=None):
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO users (
                username, password, role, specialization,
                availability_days, availability_slots, doctor_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (username, password, role, specialization, "", "", "Available")
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, password, role, specialization,
               availability_days, availability_slots, doctor_status
        FROM users
    """)
    users = cursor.fetchall()
    conn.close()
    return users


def get_doctor_profiles():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT username, specialization, availability_days,
               availability_slots, doctor_status
        FROM users
        WHERE role = 'Doctor'
    """, conn)
    conn.close()
    return df


def update_doctor_availability(username, days, slots, doctor_status):
    conn = get_connection()
    conn.execute("""
        UPDATE users
        SET availability_days = ?, availability_slots = ?, doctor_status = ?
        WHERE username = ?
    """, (",".join(days), ",".join(slots), doctor_status, username))
    conn.commit()
    conn.close()


# ---------- APPOINTMENTS ----------
def save_appointment(patient_name, doctor_name, appointment_date, appointment_time, issue, status="Booked"):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO appointments
        (patient_name, doctor_name, appointment_date, appointment_time, issue, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (patient_name, doctor_name, appointment_date, appointment_time, issue, status)
    )
    conn.commit()
    conn.close()


def get_all_appointments():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM appointments ORDER BY appointment_date, appointment_time", conn)
    conn.close()
    return df


def get_doctor_appointments(doctor_name):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM appointments WHERE doctor_name = ? ORDER BY appointment_date, appointment_time",
        conn,
        params=(doctor_name,)
    )
    conn.close()
    return df


def get_patient_appointments(patient_name):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM appointments WHERE patient_name = ? ORDER BY appointment_date, appointment_time",
        conn,
        params=(patient_name,)
    )
    conn.close()
    return df


def update_appointment_status(appointment_id, status, actor="System"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM appointments WHERE id = ?", (appointment_id,))
    row = cursor.fetchone()
    old_status = row[0] if row else None

    cursor.execute(
        "UPDATE appointments SET status = ? WHERE id = ?",
        (status, appointment_id)
    )

    cursor.execute(
        """
        INSERT INTO audit_logs (appointment_id, actor, action, old_status, new_status, log_time)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            appointment_id,
            actor,
            "STATUS_UPDATE",
            old_status,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()


def appointment_exists(doctor_name, appointment_date, appointment_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM appointments
        WHERE doctor_name = ?
          AND appointment_date = ?
          AND appointment_time = ?
          AND status != 'Cancelled'
    """, (doctor_name, appointment_date, appointment_time))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


# ---------- PATIENT HISTORY / NOTES ----------
def save_patient_note(patient_name, doctor_name, diagnosis, prescription, follow_up_date, notes):
    conn = get_connection()
    conn.execute("""
        INSERT INTO patient_history
        (patient_name, doctor_name, diagnosis, prescription, follow_up_date, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_name,
        doctor_name,
        diagnosis,
        prescription,
        follow_up_date,
        notes,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def get_patient_history(patient_name):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT *
        FROM patient_history
        WHERE patient_name = ?
        ORDER BY created_at DESC
    """, conn, params=(patient_name,))
    conn.close()
    return df


def get_doctor_notes(doctor_name):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT *
        FROM patient_history
        WHERE doctor_name = ?
        ORDER BY created_at DESC
    """, conn, params=(doctor_name,))
    conn.close()
    return df


# ---------- AUDIT ----------
def get_audit_logs():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT *
        FROM audit_logs
        ORDER BY log_time DESC
    """, conn)
    conn.close()
    return df