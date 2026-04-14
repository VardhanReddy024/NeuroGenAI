import streamlit as st
import bcrypt
from database.db import save_user, get_users

# ---------- HASH ----------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ---------- VERIFY ----------
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# ---------- LOGIN ----------
def login():
    st.sidebar.subheader("Login")

    username = st.sidebar.text_input("Username", key="login_user")
    password = st.sidebar.text_input("Password", type="password", key="login_pass")

    if st.sidebar.button("Login"):
        users = get_users()

        for row in users:
            db_username = row[0]
            db_password = row[1]
            db_role = row[2]

            if isinstance(db_password, str):
                db_password = db_password.encode()

            if db_username == username and check_password(password, db_password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = db_username
                st.session_state["role"] = db_role
                return True

        st.sidebar.error("Invalid username or password")

    return False


# ---------- SIGNUP ----------
def signup():
    st.sidebar.subheader("Signup")

    new_user = st.sidebar.text_input("New Username", key="signup_user")
    new_pass = st.sidebar.text_input("New Password", type="password", key="signup_pass")
    new_role = st.sidebar.selectbox("Role", ["Admin", "Doctor", "Patient"])

    specialization = None
    if new_role == "Doctor":
        specialization = st.sidebar.selectbox(
            "Specialization",
            ["Cardiology", "Neurology", "Orthopedics", "General"]
        )

    if st.sidebar.button("Create Account"):
        if not new_user or not new_pass:
            st.sidebar.warning("Enter username & password")
            return

        users = get_users()

        for row in users:
            if row[0] == new_user:
                st.sidebar.error("Username already exists")
                return

        hashed = hash_password(new_pass)
        save_user(new_user, hashed, new_role, specialization)

        st.sidebar.success("Account created successfully")


# ---------- LOGOUT ----------
def logout():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None
        st.rerun()