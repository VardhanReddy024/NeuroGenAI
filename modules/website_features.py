import streamlit as st
import textwrap
import pandas as pd
import random
import time
from datetime import datetime
from database.db import save_contact_query, save_home_service, get_connection

# Automatically dedent all markdown strings to prevent Streamlit from rendering them as code blocks
_orig_markdown = st.markdown
def custom_markdown(body, *args, **kwargs):
    if isinstance(body, str):
        if kwargs.get("unsafe_allow_html"):
            body = "\n".join(line.lstrip() for line in body.splitlines())
        else:
            body = textwrap.dedent(body)
    return _orig_markdown(body, *args, **kwargs)
st.markdown = custom_markdown

def show_home():
    # ---------- JIVI HERO SECTION ----------
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(2, 6, 12, 0.9) 0%, rgba(10, 25, 41, 0.7) 100%); 
                padding: 60px 40px; border-radius: 24px; border: 1px solid rgba(0, 180, 216, 0.25); 
                margin-bottom: 35px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
                position: relative; overflow: hidden;">
        <!-- Glowing Ambient Circle Background -->
        <div style="position: absolute; width: 300px; height: 300px; background: rgba(0, 229, 168, 0.08); 
                    border-radius: 50%; filter: blur(80px); top: -100px; left: -100px; z-index: 0;"></div>
        <div style="position: absolute; width: 300px; height: 300px; background: rgba(139, 92, 246, 0.08); 
                    border-radius: 50%; filter: blur(80px); bottom: -100px; right: -100px; z-index: 0;"></div>
        
        <div style="position: relative; z-index: 1;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(0, 180, 216, 0.1); 
                        padding: 6px 16px; border-radius: 50px; border: 1px solid rgba(0, 180, 216, 0.2); 
                        color: #00B4D8; font-weight: 700; font-size: 13px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;">
                ⚡ NeuroGenAI HealthOS Platform & MedX AI
            </div>
            
            <h1 class="hero-title" style="margin-bottom: 16px; line-height: 1.15; font-size: 48px;">
                Using AI to Transform Healthcare<br>for <span style="background: linear-gradient(135deg, #00E5A8 0%, #00B4D8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">8 Billion People</span>
            </h1>
            
            <p style="color: #94A3B8; font-size: 18px; max-width: 800px; margin: 0 auto 30px auto; font-weight: 500; line-height: 1.6; font-family: 'Plus Jakarta Sans', sans-serif;">
                Advanced AI-powered clinical platform featuring our MedX Clinical Agents and HealthOS, delivering precision diagnostics, real-time hospital management, and personalized doorstep care.
            </p>
            
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 30px;">
                <div style="background: rgba(255,255,255,0.04); padding: 10px 22px; border-radius: 50px; 
                            border: 1px solid rgba(255,255,255,0.06); color: #FFFFFF; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 6px;">
                    <span style="color:#00E5A8;">●</span> 3.5 Million AI Installs
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 10px 22px; border-radius: 50px; 
                            border: 1px solid rgba(255,255,255,0.06); color: #FFFFFF; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 6px;">
                    <span style="color:#00B4D8;">●</span> 170+ Countries Supported
                </div>
                <div style="background: rgba(255,255,255,0.04); padding: 10px 22px; border-radius: 50px; 
                            border: 1px solid rgba(255,255,255,0.06); color: #FFFFFF; font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 6px;">
                    <span style="color:#BD00FF;">●</span> Global #1 Open-Source MedLLMs
                </div>
            </div>
            
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                <a href="#medx-ai-assistant" style="text-decoration: none;">
                    <div style="background: linear-gradient(135deg, #00B4D8 0%, #00E5A8 100%); color: #020617; 
                                font-weight: 800; font-size: 14px; padding: 12px 28px; border-radius: 12px; 
                                box-shadow: 0 10px 20px rgba(0, 180, 216, 0.25); cursor: pointer; transition: all 0.3s;">
                        🚀 Try MedX AI Assistant
                    </div>
                </a>
                <a href="https://wa.me/918121839444" target="_blank" style="text-decoration: none;">
                    <div style="background: rgba(255, 255, 255, 0.05); color: #FFFFFF; border: 1px solid rgba(255,255,255,0.1);
                                font-weight: 700; font-size: 14px; padding: 12px 28px; border-radius: 12px; cursor: pointer;
                                display: flex; align-items: center; gap: 8px; transition: all 0.3s;">
                        💬 Chat on WhatsApp (Free Doctor)
                    </div>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- KEY CLINICAL ENGINES GRID ----------
    st.markdown('<div class="section-title">🩺 The Clinical AI Powerhouse</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    engines = [
        {
            "icon": "🧠",
            "title": "MedX Engine",
            "subtitle": "AI Agents & HealthOS",
            "desc": "Globally recognized medical reasoning models delivering advanced real-time diagnostic support, treatment guides, and clinical workflow automation."
        },
        {
            "icon": "🎤",
            "title": "AudioX Model",
            "subtitle": "Voice AI in Indic Languages",
            "desc": "Proprietary medical speech models supporting clinical dictation in Hindi, Telugu, Tamil, and English, transcribing patient history in seconds."
        },
        {
            "icon": "🌐",
            "title": "Open Source Leader",
            "subtitle": "HuggingFace Global #1",
            "desc": "Leading global clinical research with open-source medical models trusted by thousands of researchers, scientists, and hospitals worldwide."
        }
    ]
    for col, eng in zip(cols, engines):
        with col:
            st.markdown(f"""
            <div class="interactive-card" style="min-height: 230px;">
                <div style="font-size: 38px; margin-bottom: 12px;">{eng['icon']}</div>
                <div style="color: #FFFFFF; font-size: 19px; font-weight: 800; margin-bottom: 2px; font-family: 'Outfit', sans-serif;">{eng['title']}</div>
                <div style="color: #00E5A8; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;">{eng['subtitle']}</div>
                <div style="color: #94A3B8; font-size: 13.5px; line-height: 1.5; font-weight: 500;">{eng['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- INTERACTIVE CLINICAL DEMOS SECTION ----------
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        # 1. INTERACTIVE JIVI-STYLE MEDX AI DIAGNOSIS ASSISTANT
        st.markdown('<div id="medx-ai-assistant" class="section-title">⚡ MedX AI Clinical Diagnosis Assistant</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#94A3B8; font-size:14px; margin-top:-10px; margin-bottom:20px;">
            Simulate our MedX diagnostic engine. Choose a patient symptom group to generate a clinical assessment, risk category, and ICD-11 coding in real-time.
        </p>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <style>
            .stChatInputContainer {
                padding-bottom: 20px !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = [
                    {"role": "assistant", "content": "Hello! I am MedX, your AI Clinical Assistant. Please describe your symptoms or medical concerns, and I will provide a real-time preliminary assessment."}
                ]

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("Describe your symptoms (e.g., 'I have a severe headache and fever')..."):
                # Display user message in chat message container
                st.chat_message("user").markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    # Simulate stream of response with delay
                    full_response = ""
                    
                    # Basic keyword logic for the mock chatbot
                    prompt_lower = prompt.lower()
                    if "chest" in prompt_lower or "heart" in prompt_lower:
                        diagnosis = "**🚨 CRITICAL RISK: Suspected Acute Coronary Syndrome (Angina Pectoris)**\n\n*ICD-11: BA41.2*\n\n**Recommendations:**\n- Seek immediate emergency care.\n- Do not exert yourself.\n- Consult a Cardiologist immediately."
                    elif "headache" in prompt_lower or "aura" in prompt_lower:
                        diagnosis = "**⚠️ MODERATE RISK: Migraine with Visual Aura**\n\n*ICD-11: 8A80.0*\n\n**Recommendations:**\n- Rest in a quiet, dark room.\n- Stay hydrated.\n- Consult a Neurologist if symptoms persist."
                    elif "fever" in prompt_lower or "throat" in prompt_lower:
                        diagnosis = "**🟢 LOW RISK: Acute Viral/Bacterial Pharyngitis**\n\n*ICD-11: 1A03.0*\n\n**Recommendations:**\n- Rest and hydration.\n- Take over-the-counter antipyretics.\n- Consult General Medicine if fever exceeds 102°F."
                    else:
                        diagnosis = "**ℹ️ PRELIMINARY ASSESSMENT: Unspecified Symptoms**\n\nI need more information to provide a specific diagnosis. However, if you are experiencing severe pain, difficulty breathing, or sudden weakness, please visit our **24/7 Trauma Emergency** ward immediately."
                    
                    for chunk in diagnosis.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    with right_col:
        # 2. AUDIOX VOICE AI INDIC TRANSCRIBER WIDGET
        st.markdown('<div class="section-title">🎤 AudioX Voice AI - Indic Transcriber</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#94A3B8; font-size:14px; margin-top:-10px; margin-bottom:20px;">
            AudioX is our voice model optimized for medical dictation. Select an Indic language to simulate clinical voice-to-text recording.
        </p>
        """, unsafe_allow_html=True)

        with st.container():
            selected_language = st.selectbox("Select Voice AI Input Language:", [
                "Select Language...",
                "Hindi (हिन्दी)",
                "Telugu (తెలుగు)",
                "Tamil (தமிழ்)",
                "English (Medical Dictation)"
            ], key="audiox_language_selector")

            if selected_language != "Select Language...":
                record_btn = st.button("🎤 Start Voice AI Transcriber Demo", key="voice_demo_btn")
                
                # Setup dummy language recordings
                dictations = {
                    "Hindi (हिन्दी)": {
                        "original": "मुझे दो दिन से पेट में तेज दर्द हो रहा है, उल्टी जैसा भी महसूस हो रहा है और बहुत कमजोरी है।",
                        "translation": "I have been experiencing severe abdominal pain for two days, feeling nauseous, and experiencing severe weakness.",
                        "icd_code": "ICD-11: DA00.0 (Gastroenteritis of infectious origin)",
                        "dept": "General Medicine"
                    },
                    "Telugu (తెలుగు)": {
                        "original": "నాకు రెండు రోజులుగా కడుపునొప్పి ఉంది, వికారం మరియు విపరీతమైన నీరసం కూడా ఉంది.",
                        "translation": "I have abdominal pain for two days, along with nausea and extreme weakness.",
                        "icd_code": "ICD-11: DA00.0 (Gastroenteritis of infectious origin)",
                        "dept": "General Medicine"
                    },
                    "Tamil (தமிழ்)": {
                        "original": "எனக்கு இரண்டு நாட்களாக கடுமையான வயிற்று வலி உள்ளது, வாந்தி உணர்வும் பலவீனமும் இருக்கிறது.",
                        "translation": "I have severe abdominal pain for two days, with vomiting sensation and weakness.",
                        "icd_code": "ICD-11: DA00.0 (Gastroenteritis of infectious origin)",
                        "dept": "General Medicine"
                    },
                    "English (Medical Dictation)": {
                        "original": "Patient presents with persistent central chest tightness, radiating downward to the left shoulder and wrist, exacerbated by mild climbing.",
                        "translation": "Clinical notes confirm suspected Angina Pectoris / Coronary insufficiency.",
                        "icd_code": "ICD-11: BA41.2 (Angina pectoris)",
                        "dept": "Cardiology"
                    }
                }

                if record_btn:
                    # Interactive pulsing waveform during simulated recording
                    st.markdown("""
                    <div style="background: rgba(10, 25, 41, 0.4); border: 1px solid rgba(0, 229, 168, 0.2); 
                                border-radius: 12px; padding: 15px; margin-top:10px; text-align:center;">
                        <span style="color:#00E5A8; font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:1px; display:block; margin-bottom:5px;">
                            🎤 AudioX Recording...
                        </span>
                        <div class="waveform-container">
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                            <div class="waveform-bar active"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("Processing medical voice patterns..."):
                        time.sleep(1.5) # Simulating voice analysis
                    
                    data = dictations[selected_language]
                    st.markdown(f"""
                    <div style="background: rgba(5, 12, 24, 0.8); border: 1px solid rgba(139, 92, 246, 0.25); 
                                border-radius: 16px; padding: 20px; margin-top: 15px;">
                        <h5 style="color:#BD00FF; margin-top:0; margin-bottom:12px; font-weight:800; font-family:'Outfit', sans-serif;">
                            ✨ AudioX Clinical Transcription
                        </h5>
                        
                        <div style="margin-bottom:12px;">
                            <span style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase;">Captured Voice (Original)</span>
                            <blockquote style="margin: 4px 0; color:#FFFFFF; font-size:13.5px; font-style:italic; border-left: 2px solid #BD00FF; padding-left:10px;">
                                "{data['original']}"
                            </blockquote>
                        </div>
                        
                        <div style="margin-bottom:12px;">
                            <span style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase;">Clinical translation</span>
                            <div style="color:#CBD5E1; font-size:13px; font-weight:500; margin-top:2px;">{data['translation']}</div>
                        </div>
                        
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-top:14px;
                                    background:rgba(255,255,255,0.03); padding:8px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.05);">
                            <div>
                                <span style="font-size:10px; color:#64748B; font-weight:700; text-transform:uppercase; display:block;">Coded Tag</span>
                                <span style="color:#00B4D8; font-size:12px; font-weight:700;">{data['icd_code']}</span>
                            </div>
                            <div>
                                <span style="font-size:10px; color:#64748B; font-weight:700; text-transform:uppercase; display:block;">Target Specialty</span>
                                <span style="color:#00E5A8; font-size:12px; font-weight:700;">{data['dept']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="border: 1px dashed rgba(255,255,255,0.1); border-radius:20px; padding: 40px; text-align:center; margin-top: 10px;">
                    <span style="font-size:42px; display:block; margin-bottom:10px;">🎙️</span>
                    <span style="color:#64748B; font-size:14px; font-weight:600; display:block;">Select a Voice AI Language from the dropdown above to test AudioX!</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 40px 0;'>", unsafe_allow_html=True)

    # ---------- 3. HEALTHOS LIVE CAPACITY & URGENCY INDICATOR ----------
    st.markdown('<div class="section-title">📊 HealthOS Live capacity & Emergency Indicator</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94A3B8; font-size:14px; margin-top:-10px; margin-bottom:20px;">
        See real-time occupancy loads and waiting periods in our critical departments synced with the hospital HealthOS.
    </p>
    """, unsafe_allow_html=True)
    
    # Session state for simulator data so it persists or updates on request
    if "sim_data" not in st.session_state:
        st.session_state["sim_data"] = {
            "Cardiology": {"occ": 82, "wait": "12 min", "status": "Busy", "color": "#FFB703"},
            "Neurology": {"occ": 45, "wait": "5 min", "status": "Optimal", "color": "#00E5A8"},
            "Orthopedics": {"occ": 68, "wait": "18 min", "status": "Moderate", "color": "#00B4D8"},
            "Pediatrics": {"occ": 28, "wait": "3 min", "status": "Available", "color": "#00E5A8"},
            "Oncology": {"occ": 72, "wait": "25 min", "status": "High Demand", "color": "#FFB703"},
            "Emergency": {"occ": 94, "wait": "2 min", "status": "🚨 Critical Care Only", "color": "#FF4D4D"}
        }

    sim_cols = st.columns(3)
    dept_names = list(st.session_state["sim_data"].keys())
    
    for idx, d_name in enumerate(dept_names):
        info = st.session_state["sim_data"][d_name]
        with sim_cols[idx % 3]:
            st.markdown(f"""
            <div style="background: rgba(10, 25, 41, 0.4); border: 1px solid rgba(255,255,255,0.05); 
                        border-radius: 16px; padding: 18px; margin-bottom: 15px; position: relative;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="color: #FFFFFF; font-weight: 700; font-size: 16px;">{d_name}</span>
                    <span style="color: {info['color']}; font-weight: 800; font-size: 11px; text-transform: uppercase; 
                                 background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 20px;">
                        {info['status']}
                    </span>
                </div>
                <div style="color: #94A3B8; font-size: 12px; margin-bottom: 6px;">
                    Occupancy: <strong>{info['occ']}%</strong> | Est. Wait: <strong>{info['wait']}</strong>
                </div>
                <div class="custom-progress-bar">
                    <div class="custom-progress-value" style="width: {info['occ']}%; background-color: {info['color']};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    # Interactive button to trigger live simulation
    sim_btn_cols = st.columns([1, 2, 1])
    with sim_btn_cols[1]:
        if st.button("🔄 Fetch Fresh Real-time Capacity Feed", key="resimulate_feed_btn"):
            for d in dept_names:
                occ = random.randint(20, 98)
                wait = f"{random.randint(1, 40)} min"
                if occ < 40:
                    status, color = "Available", "#00E5A8"
                elif occ < 70:
                    status, color = "Optimal", "#00B4D8"
                elif occ < 85:
                    status, color = "Busy", "#FFB703"
                else:
                    status, color = "🚨 Urgent Care Prioritized", "#FF4D4D"
                st.session_state["sim_data"][d] = {"occ": occ, "wait": wait, "status": status, "color": color}
            st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 40px 0;'>", unsafe_allow_html=True)

    # ---------- JIVI PATIENT REVIEWS / TESTIMONIALS ----------
    st.markdown('<div class="section-title" style="justify-content:center; font-size:24px;">🌟 Real AI-Powered Healing Stories</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94A3B8; font-size:14.5px; text-align:center; margin-top:-10px; margin-bottom:30px; max-width:600px; margin-left:auto; margin-right:auto;">
        Hear how patients and hospital administrators leverage NeuroGenAI HealthOS & MedX to simplify diagnostic loops and secure world-class wellness.
    </p>
    """, unsafe_allow_html=True)

    testi_cols = st.columns(3)
    testimonials = [
        {
            "author": "Anjali Sharma",
            "role": "General Patient, AI Nutritionist loop",
            "text": "Jivi's AI-powered nutritionist personalized my meal plan to fit my lifestyle and health goals. It adapts to my activity and preferences, making healthy eating effortless, enjoyable, and easy to follow.",
            "avatar": "AS"
        },
        {
            "author": "Dr. Ananya Sen",
            "role": "Chief Health Administrator",
            "text": "The real-time patient analytics dashboard is outstanding. As an administrator, having instant access to live hospital efficiency, bed occupancy ratios, and patient lengths of stay helps us make critical staffing adjustments instantly.",
            "avatar": "DA"
        },
        {
            "author": "Rajesh Mehta",
            "role": "Son of Patient, Home Nursing Service",
            "text": "NeuroGenAI's Home Care Service was a lifesaver for my mother after her knee replacement surgery. The physical therapist came straight to our house, and the recovery was extremely smooth. Truly a premium experience!",
            "avatar": "RM"
        }
    ]

    for col, t in zip(testi_cols, testimonials):
        with col:
            st.markdown(f"""
            <div style="background: rgba(10, 25, 41, 0.4); border: 1px solid rgba(255,255,255,0.05); 
                        border-radius: 20px; padding: 22px; min-height: 250px; position: relative;">
                <span style="font-size: 54px; color: rgba(0, 180, 216, 0.1); position: absolute; top: -5px; left: 10px; font-family: serif; line-height: 1;">“</span>
                <p style="color: #CBD5E1; font-size: 13.5px; font-style: italic; line-height: 1.6; margin-left: 10px; z-index: 1; position: relative;">
                    {t['text']}
                </p>
                <div style="margin-top: 15px; display: flex; align-items: center; gap: 10px; margin-left: 10px;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #00B4D8, #00E5A8); display: flex; 
                                align-items: center; justify-content: center; color: #020617; font-weight: 800; font-size: 12px;">
                        {t['avatar']}
                    </div>
                    <div>
                        <div style="color: #FFFFFF; font-size: 13px; font-weight: 700;">{t['author']}</div>
                        <div style="color: #64748B; font-size: 11px; font-weight: 500;">{t['role']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 40px 0;'>", unsafe_allow_html=True)

    # ---------- JIVI FOUNDERS / LEADERSHIP SECTION ----------
    st.markdown('<div class="section-title" style="justify-content:center; font-size:24px;">👥 Founded by Proven Innovators</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94A3B8; font-size:14.5px; text-align:center; margin-top:-10px; margin-bottom:30px;">
        Bringing together world-class experience in AI, medicine, and billion-dollar venture scaling.
    </p>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 1.5, 1])
    f = {
        "name": "Vardhan Kumar Reddy",
        "title": "CEO & Founder",
        "cred": "Tech Visionary | AI Developer | Entrepreneur",
        "desc": "Passionate about leveraging artificial intelligence to transform modern healthcare and build scalable, user-centric medical solutions."
    }

    with center_col:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(10, 25, 41, 0.6) 0%, rgba(2, 6, 12, 0.8) 100%); 
                    border: 1px solid rgba(0, 180, 216, 0.15); border-radius: 20px; padding: 24px; text-align: center; height: 100%;">
            <div style="width: 60px; height: 60px; border-radius: 50%; background: rgba(0, 180, 216, 0.1); 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-size: 28px;">
                👤
            </div>
            <h4 style="color: #FFFFFF; font-size: 18px; font-weight: 800; margin: 0 0 2px 0; font-family: 'Outfit', sans-serif;">{f['name']}</h4>
            <div style="color: #00E5A8; font-size: 12px; font-weight: 700; margin-bottom: 6px;">{f['title']}</div>
            <div style="color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">{f['cred']}</div>
            <p style="color: #94A3B8; font-size: 13px; line-height: 1.5; margin: 0; font-weight: 500;">
                {f['desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- FOOTER ----------
    st.markdown("""
    <div style="text-align: center; padding: 25px 0; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 40px; color: #64748B; font-size: 12px;">
        © 2026 NeuroGenAI AI. All rights reserved. Built with advanced MedX Clinical Intelligence & ❤️ for global healthcare.
    </div>
    """, unsafe_allow_html=True)

def show_services():
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(2, 6, 12, 0.8) 0%, rgba(10, 25, 41, 0.5) 100%); 
                padding: 40px; border-radius: 20px; border: 1px solid rgba(0, 229, 168, 0.2); 
                margin-bottom: 30px; text-align: center;">
        <h1 style="color: #FFFFFF; font-size: 38px; font-family: 'Outfit', sans-serif; font-weight: 800; margin-bottom: 8px;">
            🏥 MedX AI-Scheduled <span style="background: linear-gradient(135deg, #00E5A8 0%, #00B4D8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Clinical Offerings</span>
        </h1>
        <p style="color: #94A3B8; font-size: 16px; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Leveraging our intelligent clinical HealthOS routing system to deliver super-specialty hospital care and high-fidelity, optimized doorstep healthcare.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:22px; margin-bottom:15px;">🌐 Explore Our Specialized Offerings</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏛️ MedX Super-Specialty Wards", "🏡 Premium AI-Routed Home Care"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        depts = [
            {"icon": "❤️", "title": "Cardiology Wards", "desc": "MedX-augmented coronary diagnostics, interventional procedures, smart pacemaker clinics, and expert cardiology care."},
            {"icon": "🧠", "title": "Neurology & Brain Care", "desc": "Advanced treatment for strokes, neuro-degenerative diseases, neural mapping, and intricate neurological surgery loops."},
            {"icon": "🦴", "title": "Orthopedics & Joint Rehab", "desc": "High-fidelity joint replacements, fracture healing schedules, arthritis therapy, and MedX physical rehabilitation plans."},
            {"icon": "👶", "title": "Smart Pediatrics", "desc": "Round-the-clock intensive neonatology wards, expert pediatric surgeons, and friendly, stress-free consulting modules."},
            {"icon": "🎗️", "title": "Oncology Centre", "desc": "Integrated biological cancer therapies, high-precision radiation mapping, clinical tumor boards, and home recovery checkups."},
            {"icon": "🚨", "title": "24/7 Trauma Emergency", "desc": "HealthOS-guided emergency ambulance dispatch, fully equipped trauma centers, and instantaneous surgical availability."}
        ]
        for i, dept in enumerate(depts):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="interactive-card" style="min-height: 200px; margin-bottom: 20px;">
                    <div style="font-size: 32px; margin-bottom: 12px;">{dept['icon']}</div>
                    <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-bottom: 6px; font-family: 'Outfit', sans-serif;">{dept['title']}</div>
                    <div style="color: #94A3B8; font-size: 13px; line-height: 1.5; font-weight: 500;">{dept['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
                
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(0, 229, 168, 0.05); border: 1px solid rgba(0, 229, 168, 0.25); 
                    border-radius: 16px; padding: 20px 24px; margin-bottom: 25px;">
            <h4 style="color: #00E5A8; margin-top: 0; margin-bottom: 4px; font-size: 16px; font-family: 'Outfit', sans-serif;">🏡 HealthOS Home Health Revolution</h4>
            <p style="color: #CBD5E1; font-size: 13.5px; line-height: 1.5; margin: 0;">
                Get premium healthcare delivered directly to your doorstep. Perfect for senior citizens, post-operative recovery, chronic disease management, and busy professionals. Our clinical HealthOS schedules and optimizes doorstep routes so our certified clinical staff can visit your home exactly when needed.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Home services list
        h_cols = st.columns(4)
        home_services = [
            {"icon": "🩺", "title": "Home Nursing Care", "desc": "Certified nurses for continuous monitoring, medication administration, injections, dressings, and general clinical support."},
            {"icon": "🧪", "title": "At-Home Lab Tests", "desc": "Doorstep sample collections (blood, urine, genetic profiles) with certified digital reports delivered via email in <12 hours."},
            {"icon": "🧘", "title": "Home Physiotherapy", "desc": "Pain relief therapy, post-stroke exercises, joint movement recovery sessions guided by specialized physiotherapists."},
            {"icon": "👴", "title": "Elderly Companion Care", "desc": "Specialized health assistance, companion monitoring, physical mobility support, and emergency checkups for seniors."}
        ]
        
        for i, service in enumerate(home_services):
            with h_cols[i]:
                st.markdown(f"""
                <div class="interactive-card" style="min-height: 240px; margin-bottom: 25px; border-color: rgba(0,229,168,0.15) !important;">
                    <div style="font-size: 32px; margin-bottom: 12px;">{service['icon']}</div>
                    <div style="color: #00E5A8; font-size: 16px; font-weight: 700; margin-bottom: 6px; font-family: 'Outfit', sans-serif;">{service['title']}</div>
                    <div style="color: #94A3B8; font-size: 12.5px; line-height: 1.5; font-weight: 500;">{service['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Interactive Booking Form
        st.markdown("""
        <div class="section-title" style="margin-bottom:8px;">📅 Book an AI-Scheduled Doorstep Service</div>
        <p style="color:#94A3B8; font-size:13.5px; margin-top:-6px; margin-bottom:20px;">
            Fill out the request form below. Our coordination system will allocate the closest certified home medical executive in under 15 minutes.
        </p>
        """, unsafe_allow_html=True)

        with st.container():
            with st.form("home_service_form"):
                f_cols = st.columns(3)
                with f_cols[0]:
                    p_name = st.text_input("Patient Full Name", key="hs_name", placeholder="e.g. John Doe")
                with f_cols[1]:
                    p_phone = st.text_input("Phone Number", key="hs_phone", placeholder="e.g. +91 98765 43210")
                with f_cols[2]:
                    s_type = st.selectbox("Select Service Type", [
                        "Home Nursing Care", 
                        "At-Home Lab Tests", 
                        "Home Physiotherapy", 
                        "Elderly Companion Care"
                    ], key="hs_type")

                f_cols2 = st.columns([1, 2])
                with f_cols2[0]:
                    s_date = st.date_input("Preferred Date", value=datetime.today())
                with f_cols2[1]:
                    s_address = st.text_input("Detailed Home Address", key="hs_address", placeholder="Flat/House No, Building, Street, City")

                hs_submit = st.form_submit_button("Book Home Service Appointment")

                if hs_submit:
                    if not p_name or not p_phone or not s_address:
                        st.warning("⚠️ Please provide all patient, phone, and address details.")
                    else:
                        try:
                            save_home_service(p_name, s_type, s_date.strftime("%Y-%m-%d"), p_phone, s_address)
                            st.markdown(f"""
                            <div style="background: rgba(0, 229, 168, 0.08); border: 1px solid #00E5A8; 
                                        border-radius: 12px; padding: 18px; margin-top: 15px; text-align: center;">
                                <h4 style="color: #00E5A8; margin-top: 0; margin-bottom: 6px; font-family: 'Outfit', sans-serif;">🎉 Doorstep Visit Registered!</h4>
                                <p style="color: #CBD5E1; font-size: 13.5px; margin: 0; line-height: 1.4;">
                                    Thank you, <strong>{p_name}</strong>. Your doorstep service for <strong>{s_type}</strong> on <strong>{s_date.strftime("%A, %b %d, %Y")}</strong> has been scheduled via NeuroGenAI HealthOS. A clinical executive will contact you shortly on <strong>{p_phone}</strong> to confirm.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error booking service: {e}")

def show_contact():
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(2, 6, 12, 0.8) 0%, rgba(10, 25, 41, 0.5) 100%); 
                padding: 40px; border-radius: 20px; border: 1px solid rgba(0, 180, 216, 0.2); 
                margin-bottom: 30px; text-align: center;">
        <h1 style="color: #FFFFFF; font-size: 38px; font-family: 'Outfit', sans-serif; font-weight: 800; margin-bottom: 8px;">
            📞 Connect With <span style="background: linear-gradient(135deg, #00B4D8 0%, #00E5A8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">NeuroGenAI AI</span>
        </h1>
        <p style="color: #94A3B8; font-size: 16px; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Have inquiries about our MedX diagnostic platform, hospital clinical boards, or emergency logistics? Our staff is available 24/7.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("""
        <div class="section-title" style="margin-bottom:20px;">📌 Contact Information</div>
        
        <div style="display: flex; gap: 15px; align-items: flex-start; margin-bottom: 22px;">
            <div style="background: rgba(0, 180, 216, 0.1); border: 1px solid rgba(0, 180, 216, 0.3);
                        width: 48px; height: 48px; border-radius: 12px; display: flex; 
                        align-items: center; justify-content: center; font-size: 20px;">
                🏢
            </div>
            <div>
                <h5 style="color: #FFFFFF; margin: 0 0 4px 0; font-size: 15px; font-weight: 700; font-family:'Outfit', sans-serif;">NeuroGenAI AI Main Campus</h5>
                <p style="color: #94A3B8; margin: 0; font-size: 13.5px; line-height: 1.4;">
                    NeuroGenAI Clinic, Door No. 1/20,<br>
                    Pulivendula, Kadapa Dist, AP State, India - 516390
                </p>
            </div>
        </div>

        <div style="display: flex; gap: 15px; align-items: flex-start; margin-bottom: 22px;">
            <div style="background: rgba(0, 229, 168, 0.1); border: 1px solid rgba(0, 229, 168, 0.3);
                        width: 48px; height: 48px; border-radius: 12px; display: flex; 
                        align-items: center; justify-content: center; font-size: 20px;">
                📞
            </div>
            <div>
                <h5 style="color: #FFFFFF; margin: 0 0 4px 0; font-size: 15px; font-weight: 700; font-family:'Outfit', sans-serif;">Phone & Emergency Hotline</h5>
                <p style="color: #94A3B8; margin: 0; font-size: 13.5px; line-height: 1.4;">
                    Support Helpline: <strong>+1 (800) 273-7857</strong><br>
                    Emergency Hotline: <strong>+1 (800) 911-CARE</strong> (24/7 Toll-Free)
                </p>
            </div>
        </div>

        <div style="display: flex; gap: 15px; align-items: flex-start; margin-bottom: 22px;">
            <div style="background: rgba(255, 183, 3, 0.1); border: 1px solid rgba(255, 183, 3, 0.3);
                        width: 48px; height: 48px; border-radius: 12px; display: flex; 
                        align-items: center; justify-content: center; font-size: 20px;">
                ✉️
            </div>
            <div>
                <h5 style="color: #FFFFFF; margin: 0 0 4px 0; font-size: 15px; font-weight: 700; font-family:'Outfit', sans-serif;">Email & Clinical Queries</h5>
                <p style="color: #94A3B8; margin: 0; font-size: 13.5px; line-height: 1.4;">
                    General Enquiries: <strong>info@neurogenai.com</strong><br>
                    Online Booking Support: <strong>bookings@neurogenai.com</strong>
                </p>
            </div>
        </div>
        
        <div style="display: flex; gap: 15px; align-items: flex-start;">
            <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3);
                        width: 48px; height: 48px; border-radius: 12px; display: flex; 
                        align-items: center; justify-content: center; font-size: 20px;">
                🕒
            </div>
            <div>
                <h5 style="color: #FFFFFF; margin: 0 0 4px 0; font-size: 15px; font-weight: 700; font-family:'Outfit', sans-serif;">Operation Hours</h5>
                <p style="color: #94A3B8; margin: 0; font-size: 13.5px; line-height: 1.4;">
                    Outpatient Clinic: <strong>8:00 AM - 8:00 PM (Mon-Sat)</strong><br>
                    Emergency Wards: <strong>24 Hours / 365 Days</strong>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-title" style="margin-bottom:15px;">✉️ Send Us a Query</div>
        <p style="color:#94A3B8; font-size:14px; margin-top:-10px; margin-bottom:20px;">
            Submit your questions directly to our support team and receive a professional response via email.
        </p>
        """, unsafe_allow_html=True)
        
        with st.container():
            with st.form("contact_form"):
                c_name = st.text_input("Your Full Name", key="c_name", placeholder="e.g. Sarah Jenkins")
                c_email = st.text_input("Email Address", key="c_email", placeholder="e.g. sarah@example.com")
                c_subject = st.text_input("Subject", key="c_subject", placeholder="e.g. Preventive Health Checkups package query")
                c_msg = st.text_area("Message Detail", key="c_message", placeholder="Type your detailed message here...", height=120)
                
                submitted = st.form_submit_button("Submit Query Form")
                
                if submitted:
                    if not c_name or not c_email or not c_msg:
                        st.warning("⚠️ Name, Email, and Message detail are required.")
                    elif "@" not in c_email:
                        st.warning("⚠️ Please provide a valid email address.")
                    else:
                        try:
                            save_contact_query(c_name, c_email, c_subject, c_msg)
                            st.markdown(f"""
                            <div style="background: rgba(0, 180, 216, 0.08); border: 1px solid #00B4D8; 
                                        border-radius: 12px; padding: 18px; margin-top: 15px; text-align: center;">
                                <h4 style="color: #00B4D8; margin-top: 0; margin-bottom: 6px; font-family:'Outfit', sans-serif;">🎉 Ticket Received Successfully!</h4>
                                <p style="color: #CBD5E1; font-size: 13.5px; margin: 0; line-height: 1.4;">
                                    Thank you, <strong>{c_name}</strong>. Your query about <strong>"{c_subject if c_subject else 'General Enquiry'}"</strong> has been registered. Our support desk will reply to you at <strong>{c_email}</strong> within 4 hours.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error submitting query: {e}")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 40px 0;'>", unsafe_allow_html=True)

    # 4. INTERACTIVE DYNAMIC RATING & FEEDBACK WIDGET
    st.markdown('<div class="section-title">⭐ Interactive Patient Feedback & Experience Rating</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#94A3B8; font-size:14px; margin-top:-10px; margin-bottom:20px;">
        Slide to select your care satisfaction score and watch the clinical sentiment shift in real-time!
    </p>
    """, unsafe_allow_html=True)
    
    with st.container():
        f_cols = st.columns([1.2, 1])
        with f_cols[0]:
            rating_score = st.slider("Select your satisfaction score (1 to 5 Stars):", 1, 5, 5, key="fb_rating_score")
            fb_comments = st.text_area("Your general feedback or clinical experience (Optional):", key="fb_comments", placeholder="Tell us how we can make your next clinical visit even better...")
            
            if st.button("Submit My Experience Rating", key="fb_submit_btn"):
                st.markdown(f"""
                <div style="background: rgba(0, 229, 168, 0.08); border: 1px solid #00E5A8; 
                            border-radius: 12px; padding: 18px; margin-top: 15px; text-align: center;">
                    <h4 style="color: #00E5A8; margin-top: 0; margin-bottom: 6px;">🎉 Feedback Received!</h4>
                    <p style="color: #CBD5E1; font-size: 13.5px; margin: 0; line-height: 1.4;">
                        Thank you for your rating of <strong>{rating_score} / 5 Stars</strong>! Your valuable remarks have been routed to our Chief Patient Experience Coordinator.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
        with f_cols[1]:
            # Dynamic sentiment emojis based on rating
            emoji_map = {
                1: {"emoji": "😢", "title": "Critical Support Triggered", "desc": "We are extremely sorry your experience did not meet standard clinical parameters. Our hospital relations supervisor will reach out immediately to resolve this.", "color": "#FF4D4D"},
                2: {"emoji": "😐", "title": "Opportunity to Learn", "desc": "Thank you. We are analyzing the specific points of friction. We commit to continuous workflow improvements to provide a more satisfactory clinic loop.", "color": "#FFB703"},
                3: {"emoji": "🙂", "title": "Good & Satisfactory", "desc": "Glad to know we delivered standard, reliable healthcare. We are striving to refine our logistics to make your next visit even faster and more convenient.", "color": "#00B4D8"},
                4: {"emoji": "😀", "title": "Highly Satisfied", "desc": "Excellent! We are thrilled our doctors and assistants met your expectations. Your positive feedback has been forwarded to the duty ward staff.", "color": "#00E5A8"},
                5: {"emoji": "🤩", "title": "Exemplary NeuroGenAI Standard!", "desc": "World-class! You have experienced our NeuroGenAI Gold standard of clinical dedication. Thank you for recognizing our continuous devotion to patient happiness.", "color": "#FFD700"}
            }
            active_mood = emoji_map[rating_score]
            
            st.markdown(f"""
            <div style="background: rgba(10, 25, 41, 0.4); border: 2px solid {active_mood['color']}; 
                        border-radius: 18px; padding: 25px; text-align: center; height:100%;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.15); display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div style="font-size: 72px; line-height: 1; margin-bottom: 12px;">{active_mood['emoji']}</div>
                <h4 style="color: {active_mood['color']}; margin-top:0; margin-bottom:8px; font-weight:800; font-family:'Outfit', sans-serif;">{active_mood['title']}</h4>
                <p style="color: #94A3B8; font-size:13px; line-height:1.5; margin:0; max-width:320px;">
                    {active_mood['desc']}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    # Visual Interactive Map representation
    st.markdown("""
    <div style="background: rgba(10, 25, 41, 0.4); border: 1px solid rgba(255,255,255,0.05); 
                border-radius: 24px; padding: 30px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
        <h4 style="color: #FFFFFF; margin-top: 0; margin-bottom: 15px; font-weight:700; font-family:'Outfit', sans-serif;">📍 NeuroGenAI Interactive Location Map</h4>
        <div style="background: linear-gradient(135deg, #091220, #020612); border-radius: 16px; 
                    height: 200px; display: flex; align-items: center; justify-content: center; flex-direction: column;
                    border: 1px dashed rgba(0, 180, 216, 0.4); position: relative; overflow: hidden;">
            <!-- Glow background effect -->
            <div style="position: absolute; width: 100px; height: 100px; background: rgba(0, 180, 216, 0.15); 
                        border-radius: 50%; filter: blur(40px); top: 50px; left: 50%;"></div>
            
            <div style="font-size: 40px; margin-bottom: 10px;">🗺️</div>
            <div style="color: #FFFFFF; font-weight: 700; font-size: 15px; font-family:'Outfit', sans-serif;">Pulivendula Main Campus</div>
            <p style="color: #94A3B8; font-size: 12.5px; max-width: 400px; margin: 4px auto 0 auto; line-height: 1.4;">
                Map Preview • Door No. 1/20, Pulivendula, Kadapa District, Andhra Pradesh.
            </p>
            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <span style="background: rgba(0, 229, 168, 0.15); color: #00E5A8; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px;">✓ Valet Parking Free</span>
                <span style="background: rgba(0, 180, 216, 0.15); color: #00B4D8; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px;">✓ Wheelchair Accessible</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_about():
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(2, 6, 12, 0.8) 0%, rgba(10, 25, 41, 0.5) 100%); 
                padding: 40px; border-radius: 20px; border: 1px solid rgba(0, 180, 216, 0.2); 
                margin-bottom: 30px; text-align: center;">
        <h1 style="color: #FFFFFF; font-size: 38px; font-family: 'Outfit', sans-serif; font-weight: 800; margin-bottom: 8px;">
            📖 About <span style="background: linear-gradient(135deg, #00B4D8 0%, #00E5A8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">NeuroGenAI AI</span>
        </h1>
        <p style="color: #94A3B8; font-size: 16px; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Discover our mission to revolutionize global healthcare through advanced Artificial Intelligence, seamless hospital logistics, and uncompromising patient care.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🚀 Our Mission & Vision</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#CBD5E1; font-size:15px; line-height:1.7; margin-bottom:20px;">
        At <strong>NeuroGenAI AI</strong>, our mission is to make world-class healthcare accessible, predictive, and efficient for everyone. We believe that Artificial Intelligence is not just a tool, but a foundational shift in how clinical assessments, hospital logistics, and patient wellness are managed.
    </p>
    <p style="color:#CBD5E1; font-size:15px; line-height:1.7; margin-bottom:40px;">
        Our vision is to empower doctors with hyper-accurate diagnostic models (MedX), while giving patients full transparency and control over their healthcare journey through an intuitive HealthOS portal.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🏥 The NeuroGenAI Advantage</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    advantages = [
        {"icon": "⚡", "title": "Real-Time AI Diagnostics", "desc": "MedX models reason in milliseconds, assisting our doctors to make the most accurate clinical decisions faster than ever before."},
        {"icon": "🛡️", "title": "Uncompromised Data Security", "desc": "Your medical records are encrypted and protected by enterprise-grade security protocols, ensuring total patient privacy."},
        {"icon": "🌍", "title": "Global HealthOS Ecosystem", "desc": "From in-house ICU management to seamless doorstep physiotherapy, our digital ecosystem covers every aspect of health."}
    ]
    
    for col, adv in zip(cols, advantages):
        with col:
            st.markdown(f"""
            <div class="interactive-card" style="min-height: 200px; margin-bottom: 20px;">
                <div style="font-size: 32px; margin-bottom: 12px;">{adv['icon']}</div>
                <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-bottom: 6px; font-family: 'Outfit', sans-serif;">{adv['title']}</div>
                <div style="color: #94A3B8; font-size: 13px; line-height: 1.5; font-weight: 500;">{adv['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 40px 0;'>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">❓ Frequently Asked Questions (FAQ)</div>', unsafe_allow_html=True)
    
    faq_data = [
        {"q": "How accurate is the MedX AI Assistant?", "a": "MedX is trained on millions of clinical data points and achieves over 96.8% accuracy on standard diagnostic benchmarks. However, it is an assistive tool and all final diagnoses are made by our certified human doctors."},
        {"q": "Can I book a doorstep home service anytime?", "a": "Yes! Our platform is available 24/7. Simply navigate to the 'Services' section, fill out your details, and a medical professional will be dispatched based on availability."},
        {"q": "Is my data safe with NeuroGenAI?", "a": "Absolutely. We employ end-to-end encryption and comply with global health data privacy standards (such as HIPAA). Your data is never shared without your explicit consent."},
        {"q": "How do I contact the emergency ward?", "a": "You can immediately call our 24/7 Emergency Hotline at +1 (800) 911-CARE, or use the Contact Us page for non-urgent clinical queries."}
    ]
    
    for faq in faq_data:
        with st.expander(f"**{faq['q']}**"):
            st.markdown(f"<p style='color:#CBD5E1; font-size:14px; margin-top:10px;'>{faq['a']}</p>", unsafe_allow_html=True)
            
    st.markdown("<br><br>", unsafe_allow_html=True)
