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
    # Render CarePulse Shield Logo & Brand Headers
    st.markdown("""
    <div class="logo-container">
        <div class="logo-header">
            <div class="logo-icon">
                <svg width="42" height="42" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <!-- Dark slate shield background with glowing teal border -->
                    <path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 17 12 22 12 22Z" fill="#1E293B" stroke="#00B4D8" stroke-width="2" stroke-linejoin="round"/>
                    <!-- Green/teal medical cross -->
                    <path d="M12 8V16M8 12H16" stroke="#00E5A8" stroke-width="3" stroke-linecap="round"/>
                </svg>
            </div>
            <div class="logo-text">Care<span>Pulse</span></div>
        </div>
        <div class="logo-subtext">H o s p i t a l</div>
        <div class="logo-tagline">Sign in to continue to NeuroGenAI App.</div>
    </div>
    """, unsafe_allow_html=True)

    # Email/Username Input
    username = st.text_input(
        "Username",
        key="login_user",
        placeholder="Email"
    )

    # Password Input
    password = st.text_input(
        "Password",
        type="password",
        key="login_pass",
        placeholder="Password"
    )

    # Checkbox and Forgot Password Link Row
    col1, col2 = st.columns([1, 1])
    with col1:
        st.checkbox("Remember Me", value=False, key="remember_me")
    with col2:
        st.markdown('<div style="text-align: right; margin-top: 4px;"><a href="#" class="forgot-pass-link">Forgot Password?</a></div>', unsafe_allow_html=True)

    # Sign In Button (Primary)
    if st.button("SIGN IN", type="primary", key="login_btn"):
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
                st.success(f"Welcome, {db_username}!")
                return True

        st.error("Invalid username or password.")

    # Bottom Navigation / Toggle (Secondary outlined action)
    st.markdown('<div style="text-align: center; margin-top: 24px; font-size: 14px; color: #64748B;">Don\'t have an account?</div>', unsafe_allow_html=True)
    if st.button("Sign Up", type="secondary", key="toggle_to_signup"):
        st.session_state["auth_mode"] = "signup"
        st.rerun()

    return False


# ---------- SIGNUP ----------
def signup():
    st.markdown("""
    <div class="logo-container">
        <div class="logo-header">
            <div class="logo-icon">
                <svg width="42" height="42" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 17 12 22 12 22Z" fill="#1E293B" stroke="#00B4D8" stroke-width="2" stroke-linejoin="round"/>
                    <path d="M12 8V16M8 12H16" stroke="#00E5A8" stroke-width="3" stroke-linecap="round"/>
                </svg>
            </div>
            <div class="logo-text">Care<span>Pulse</span></div>
        </div>
        <div class="logo-subtext">Hospital</div>
        <div class="logo-tagline">Create your NeuroGenAI account.</div>
    </div>
    """, unsafe_allow_html=True)


    # Username Input
    new_user = st.text_input(
        "New Username",
        key="signup_user",
        placeholder="Choose a username"
    )

    # Password Input
    new_pass = st.text_input(
        "New Password",
        type="password",
        key="signup_pass",
        placeholder="Create a password"
    )

    # Role Selection
    new_role = st.selectbox(
        "Role",
        ["Admin", "Doctor", "Patient"],
        key="signup_role"
    )

    # Specialized Options for Doctors
    specialization = None
    if new_role == "Doctor":
        specialization = st.selectbox(
            "Specialization",
            ["Cardiology", "Neurology", "Orthopedics", "General"],
            key="signup_specialization"
        )

    # Create Account Button (Primary)
    if st.button("CREATE ACCOUNT", type="primary", key="signup_btn"):
        if not new_user or not new_pass:
            st.warning("Please enter username and password.")
            return

        users = get_users()

        for row in users:
            if row[0] == new_user:
                st.error("Username already exists.")
                return

        hashed = hash_password(new_pass)
        save_user(new_user, hashed, new_role, specialization)

        st.success("Account created successfully! Please sign in.")
        st.session_state["auth_mode"] = "login"
        st.rerun()

    # Bottom Navigation / Toggle (Secondary outlined action)
    st.markdown('<div style="text-align: center; margin-top: 24px; font-size: 14px; color: #64748B;">Already have an account?</div>', unsafe_allow_html=True)
    if st.button("Log In", type="secondary", key="toggle_to_login"):
        st.session_state["auth_mode"] = "login"
        st.rerun()


# ---------- LOGOUT ----------
def logout():
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None
        st.session_state["show_login_form"] = False
        st.session_state["auth_mode"] = "login"
        st.rerun()