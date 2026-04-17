import streamlit as st
from db import update_user_progress

def render_doctors_hub(username):
    st.title("🩺 The Doctors AI Hub")
    st.markdown("### *Learn AI or get left behind by the system.*")
    st.write("Healthcare systems are pivoting to AI. As a clinician, you must master these tools to maintain operational superiority.")
    
    st.divider()
    
    st.markdown("### 1. Core Medical AI Training")
    st.write("Start here to build your clinical foundation in Applied Artificial Intelligence.")
    
    # Course 1
    with st.expander("🤖 ChatGPT for Clinical Drafts", expanded=True):
        st.write("Write referral letters, SOAP notes, and analyze basic PDFs securely.")
        # Fix: Now passing username AND course name correctly to avoid database crash
        if st.button("Start Course: Clinical Drafts", key="doc_course_1"):
            update_user_progress(username, "ChatGPT for Clinical Drafts", 10.0)
            st.success("Course Started! Progress saved. Head to your Workspace.")

    # Course 2
    with st.expander("📊 Data Extraction for EHR Pipelines"):
        st.write("Automating data extraction pipelines using strict HIPAA-compliant protocols.")
        if st.button("Start Course: EHR Pipelines", key="doc_course_2"):
            update_user_progress(username, "Data Extraction for EHR Pipelines", 10.0)
            st.success("Course Started! Progress saved.")
            
    st.divider()
    
    st.markdown("### 2. Medical AI Projects (Build with Mentor)")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Project 1: Clinical Appointment Bot**\n\nBuild a smart AI to manage OPD bookings 24/7.")
    with col2:
        st.info("**Project 2: Medical Report Analyzer**\n\nBuild an AI to simplify complex lab reports for patients.")