import streamlit as st
import os
from dotenv import load_dotenv
import time # Added for typing effect

# Load environment variables first
load_dotenv()

from auth import main as auth_main
from school_workspace import render_dashboard
from admin_panel import render_admin_dashboard
from db import init_db
from multi_agent_engine import ClassroomOrchestrator

st.set_page_config(page_title="Bharat AI School", page_icon="🏫", layout="wide")

# Initialize orchestrator instance
orchestrator = ClassroomOrchestrator()

def main():
    # Initialize database tables if they do not exist
    init_db()

    # ---------------- STRICT ROUTER LOGIC ----------------
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        # IF NOT LOGGED IN: Entirely restrict to Login/Signup view
        auth_main()
    else:
        # IF LOGGED IN: Entirely restrict to Application view (hide login page)

        # Show Sidebar Navigation
        st.sidebar.title("Navigation")
        st.sidebar.write(f"Logged in as: **{st.session_state.get('username', '')}** ({st.session_state.get('role', 'student').capitalize()})")

        # Navigation Buttons
        if st.sidebar.button("Student Dashboard", use_container_width=True):
            st.session_state['current_page'] = 'Dashboard'

        if st.sidebar.button("👨‍💻 AI Project Mentor", use_container_width=True):
            st.session_state['current_page'] = 'Mentor'

        if st.sidebar.button("🩺 Doctors AI Hub", use_container_width=True):
            st.session_state['current_page'] = 'Doctors'

        # New Live AI Classroom Tab
        if st.sidebar.button("🎭 Live AI Classroom", use_container_width=True):
            st.session_state['current_page'] = 'Live Classroom'

        # Admin Panel Button (ONLY IF ADMIN)
        if st.session_state.get('role') == 'admin':
            if st.sidebar.button("Admin Panel", type="primary", use_container_width=True):
                st.session_state['current_page'] = 'Admin Panel'

        st.sidebar.divider()
        if st.sidebar.button("Logout", use_container_width=True):
            # Strict Logout Process
            st.session_state['logged_in'] = False
            for key in ['username', 'role', 'current_page', 'active_course', 'current_teacher']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # Render Content based on current_page
        page = st.session_state.get('current_page', 'Dashboard')
        if page == 'Admin Panel' and st.session_state.get('role') == 'admin':
            render_admin_dashboard()
        elif page == 'Mentor':
            from project_mentor import render_project_mentor
            render_project_mentor(st.session_state.get('username', 'Student'))
        elif page == 'Doctors':
            from doctors_hub import render_doctors_hub
            render_doctors_hub(st.session_state.get('username', 'Student'))
        elif page == 'Live Classroom':
            # ---------------------------------------------------------
            # 🎭 LIVE AI CLASSROOM (Multi-Agent Debate)
            # ---------------------------------------------------------
            st.title("🎭 Live AI Classroom")
            st.info("Experience a multi-agent debate between an AI Teacher and AI Students.")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                topic = st.text_input("Enter a Medical Topic to Learn:", placeholder="e.g., Myocardial Infarction")
            with col2:
                st.write("") # Spacing
                st.write("")
                start_btn = st.button("Start Live Class 🚀", use_container_width=True)

            if start_btn:
                if topic:
                    st.success(f"Starting Session on: {topic}")
                    st.markdown("---")
                    
                    # Fetching the script from the orchestrator
                    script = orchestrator.generate_classroom_script(topic)
                    
                    # Rendering the multi-agent chat dynamically
                    for turn in script:
                        # SHOCK ABSORBER: Do not trust the LLM's avatar string
                        role = turn.get("role", "assistant")
                        name = turn.get("name", "AI")
                        content = turn.get("content", "")

                        # Force safe default emojis to prevent Streamlit crashes
                        safe_avatar = "🧑‍🏫" if role == "assistant" else "🧑‍🎓"

                        with st.chat_message(role, avatar=safe_avatar):
                            st.markdown(f"**{name}**")
                            st.markdown(content)
                        time.sleep(1.5) # Adds a realistic "typing" delay
                else:
                    st.warning("Please enter a topic before starting the class.")
        else:
            render_dashboard(st.session_state.get('username', 'Student'))

if __name__ == '__main__':
    main()
