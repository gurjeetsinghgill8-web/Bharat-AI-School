import streamlit as st
from engine import get_ai_response
from memory import get_chat_history
from ai_teachers import get_all_teachers
from db import create_user_project, get_user_progress, update_user_progress, get_user_skill, update_user_skill, save_custom_syllabus, get_custom_syllabi
from courses_data import CURATED_COURSES
import time


def safe_rerun():
    time.sleep(0.5)
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

@st.cache_data(ttl=3600)
def generate_dynamic_projects(course_title):
    from utils.groq_client import query_groq
    prompt = f"Act as an Elite AI Architect. Generate 10 HIGH-VALUE, Real-World AI Agent project ideas for a student who just finished the course '{course_title}'. Output them as a numbered list. Keep them under 1 sentence each. Do not add intro/outro fluff."
    return query_groq([{"role": "user", "content": prompt}])

# Course Syllabus Data (V2.1 Ultimate Library)
COURSE_SYLLABUS = {
    "ChatGPT Prompt Engineering": """
**Course Syllabus:**
1. Intro to LLM APIs
2. Text Summarization & Inferring
3. Transforming Data Formats
4. Building Custom Chatbots
""",
    "ChatGPT for Entrepreneurs": """
**Course Syllabus:**
1. Idea Validation with AI
2. Automated Marketing Copy
3. Client Outreach Automation
""",
    "Prompt Strategy for Claude 3": """
**Course Syllabus:**
1. Advanced XML Tagging
2. Handling Long-context Documents
3. Sonnet vs Opus Workflows
""",
    "Google Gemini: Multimodal Mastery": """
**Course Syllabus:**
1. Vision & Image Parsing basics
2. Audio & Video Context Processing
3. Google Workspace Integrations
""",
    "Hugging Face Fastai Course": """
**Course Syllabus:**
1. Transformers Introduction
2. Understanding Pipeline APIs
3. Building with Diffusers
""",
    "Fine-tuning LLaMA 3": """
**Course Syllabus:**
1. LoRA & QLoRA Basics
2. Preparing Custom Datasets
3. Local Testing & Cloud Deployment
"""
}

def render_dashboard(username):
    st.title(f"Welcome to your Classroom, {username}! 🎓")

    # V3.1 - Onboarding Gate
    user_skill = get_user_skill(username)
    if user_skill == "Unknown":
        st.info("### Let's Personalize Your Experience 🎯")
        st.write("Before we begin, tell us your AI & Coding background so your AI Mentor can adapt.")
        selected_skill = st.selectbox(
            "Select Skill",
            ["Non-Coder", "Beginner", "Advanced/Pro"],
            key="onboarding_skill_select",
        )
        if st.button("Save & Start Learning", type="primary"):
            st.session_state["user_skill"] = selected_skill
            update_user_skill(username, selected_skill)
            safe_rerun()

        # Stop here until the user saves their skill.
        st.stop()

    # V3.1 - Top 10 Trending Sidebar
    st.sidebar.markdown("### 🔥 Trending AI Skills (Top 10)")
    trending_skills = [
        "Agentic Workflows (MCP)",
        "RAG Pipelines",
        "LLM API Integration",
        "Streamlit Frontends",
        "Groq High-Speed Inference",
        "Multimodal Vision",
        "Fine-tuning LLaMA",
        "Local LLM Hosting",
        "Prompt Engineering",
        "Autonomous Coders",
    ]
    for idx, skill in enumerate(trending_skills, start=1):
        if st.sidebar.button(f"{idx}. {skill}", key=f"trending_skill_{idx}", use_container_width=True):
            st.session_state["active_course"] = skill
            safe_rerun()

    # V4.0 - Personalized AI Guide (Custom Course Generator)
    st.sidebar.divider()
    st.sidebar.markdown("### 🎯 Create Your Custom Learning Path")
    with st.sidebar.expander("Generate My AI Path 🚀", expanded=False):
        user_profile = st.text_area(
            "Who are you and what do you want to build?",
            key="pai_user_profile",
            placeholder="Example: I am a 5th grade student and I want to learn AI basics.\nOr: I am a Cardiologist and I want to automate my clinic workflows.",
            height=120,
        )
        resource_preference = st.selectbox(
            "Select Resource Preference",
            ["Free Resources", "Paid/Premium"],
            key="pai_resource_preference",
        )

        if st.button("Generate My AI Path 🚀", type="primary", use_container_width=True):
            from engine import generate_personalized_syllabus
            with st.spinner("Creating your custom learning path..."):
                syllabus_md = generate_personalized_syllabus(user_profile, resource_preference)
                st.session_state["pai_generated_syllabus"] = syllabus_md

                # Best-effort title extraction from the first non-empty line.
                title = "My Personalized Syllabus"
                for line in (syllabus_md or "").splitlines():
                    if line.strip():
                        title = line.strip().lstrip("#").strip().strip('"').strip('*')
                        break
                st.session_state["pai_generated_title"] = title

        generated = st.session_state.get("pai_generated_syllabus")
        if generated:
            st.markdown("#### 📝 Your Custom Syllabus Preview")
            st.markdown(generated)
            if st.button("Accept & Start Course", use_container_width=True, type="primary"):
                title = st.session_state.get("pai_generated_title") or "My Personalized Syllabus"
                new_id = save_custom_syllabus(username, user_profile, title, generated)
                st.session_state["active_course"] = title
                st.session_state["active_custom_syllabus_id"] = new_id
                st.success(f"Course '{title}' started! Opening Study Room...")
                safe_rerun()

    # Quick access: Start a previously saved custom syllabus
    try:
        saved_custom = get_custom_syllabi(username)
    except Exception:
        saved_custom = []
    if saved_custom:
        with st.sidebar.expander("Your saved custom paths", expanded=False):
            for item in saved_custom[:10]:
                if st.button(f"▶ {item['custom_course_title']}", key=f"start_custom_{item['id']}", use_container_width=True):
                    st.session_state["active_course"] = item["custom_course_title"]
                    st.session_state["active_custom_syllabus_id"] = item["id"]
                    safe_rerun()

    # State variable for the active course view
    if 'active_course' not in st.session_state:
        st.session_state['active_course'] = None

    # View 1: Ultimate Course Library (V2.1) & Resume Section
    if st.session_state['active_course'] is None:
        
        # V2.1 - Pillar Issue 2: Progress Tracking & Resume Learning
        incomplete_courses = get_user_progress(username)
        if incomplete_courses:
            latest_course = incomplete_courses[0]
            st.info(f"### 👋 Welcome Back, {username}!")
            st.markdown("Pick up right where you left off:")
            
            with st.container(border=True):
                st.subheader(f"🎓 {latest_course['course_name']}")
                st.progress(int(latest_course['completion_percentage']) / 100.0)
                st.caption(f"{int(latest_course['completion_percentage'])}% Completed")
                
                if st.button("Continue Learning", key="resume_btn", type="primary"):
                    st.session_state['active_course'] = latest_course['course_name']
                    safe_rerun()
                    
            st.divider()
            
        st.markdown("### 📚 Bharat AI Pro Library")
        st.markdown("Explore top-tier curated courses from industry leaders. Master the tools and build real projects.")
        
        # V3.1 - External Course Input
        ext_col1, ext_col2 = st.columns([3, 1])
        with ext_col1:
            ext_link = st.text_input("🔗 Paste any External Course Link to track it here:", label_visibility="collapsed", placeholder="Paste any external course link to track in your dashboard...")
        with ext_col2:
            if st.button("Track Progress", use_container_width=True):
                if ext_link:
                    update_user_progress(username, f"Custom: {ext_link[:25]}...", 0.0)
                    st.toast("External course added to Tracker!")
                    safe_rerun()
                
        st.divider()
        
        tab_names = ["🌍 All", "🤖 Anthropic", "🧠 OpenAI", "🌌 Google"]
        tabs = st.tabs(tab_names)
        
        def render_course_grid(course_list, tab_key_prefix):
            for c_idx, c in enumerate(course_list):
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(c['title'])
                        st.markdown(f"**Provider:** {c['provider']} &nbsp;&nbsp;|&nbsp;&nbsp; **Level:** {c['level']}")
                        st.markdown(f"*{c['description']}*")
                        is_free = bool(c.get("is_free", False))
                        if is_free:
                            st.markdown("🔖 :green[**100% Free Official Course**]")
                        else:
                            st.markdown("👑 :orange[**Premium Pro Course**]")
                    with col2:
                        st.link_button("🌐 Open External", url=c['url'], use_container_width=True)
                        if st.button("Start Local Module", key=f"start_{tab_key_prefix}_{c['id']}", type="primary", use_container_width=True):
                            update_user_progress(username, c['title'], 10.0)
                            st.session_state['active_course'] = c['title']
                            safe_rerun()

        with tabs[0]:
            render_course_grid(CURATED_COURSES, "all")
        with tabs[1]:
            render_course_grid([c for c in CURATED_COURSES if "Anthropic" in c['provider']], "anthropic")
        with tabs[2]:
            render_course_grid([c for c in CURATED_COURSES if "OpenAI" in c['provider']], "openai")
        with tabs[3]:
            render_course_grid([c for c in CURATED_COURSES if "Google" in c['provider']], "google")

    # View 2: Active Course & Chat Interface
    else:
        active_course = st.session_state['active_course']
        
        # Back Button to return to library
        if st.button("⬅️ Back to Course Library"):
            st.session_state['active_course'] = None
            safe_rerun()
            
        st.divider()
        st.header(f"Study Room: {active_course}")
        
        # Output Syllabus
        with st.expander("📚 View Course Syllabus", expanded=True):
            syllabus_md = COURSE_SYLLABUS.get(active_course)
            if not syllabus_md:
                # If this is a custom course, fetch its syllabus from DB.
                custom_id = st.session_state.get("active_custom_syllabus_id")
                try:
                    custom_items = get_custom_syllabi(username)
                except Exception:
                    custom_items = []

                custom_match = None
                if custom_id:
                    for item in custom_items:
                        if item.get("id") == custom_id:
                            custom_match = item
                            break
                if not custom_match:
                    for item in custom_items:
                        if item.get("custom_course_title") == active_course:
                            custom_match = item
                            # Keep future renders consistent.
                            st.session_state["active_custom_syllabus_id"] = item.get("id")
                            break

                syllabus_md = (custom_match or {}).get("generated_syllabus")

            if syllabus_md:
                # V5.0 - Interactive Syllabus Parsing
                if "### Module" in syllabus_md:
                    # Split by module header but keep the header
                    import re
                    modules = re.split(r'(### Module \d+:)', syllabus_md)
                    
                    # The first element might be empty or intro text
                    if modules[0].strip():
                        st.markdown(modules[0])
                    
                    # Iterate through matches
                    for i in range(1, len(modules), 2):
                        header = modules[i]
                        content = modules[i+1] if i+1 < len(modules) else ""
                        with st.expander(f"📖 {header.replace('### ', '')}", expanded=(i==1)):
                            st.markdown(content)
                            st.checkbox("✅ Mark Module as Completed", key=f"complete_{active_course}_{i}")
                else:
                    st.markdown(syllabus_md)
            else:
                st.markdown("Syllabus not found.")

        if st.button("💡 See Career & Monetization Path", use_container_width=True):
            st.info(f"### 🚀 Career Growth for {active_course}\n\n"
                    "This course is designed to transition you from a learner to a builder. "
                    "Mastering these specific modules allows you to:\n"
                    "- Automate high-value tasks in your specific domain.\n"
                    "- Build and launch production-ready AI agents.\n"
                    "- Create new revenue streams by offering specialized AI services.")
            st.toast("Career path activated! 🎯")
            
        st.divider()
        
        # Chat Interface for the Course
        teachers = get_all_teachers()
        if 'current_teacher' not in st.session_state:
            st.session_state['current_teacher'] = teachers[0]
            
        from ai_teachers import get_teacher_info
        
        selected_teacher = st.selectbox("Choose your AI Teacher for this course:", teachers, index=teachers.index(st.session_state['current_teacher']))
        
        # Display Teacher Expertise/Description
        teacher_info = get_teacher_info(selected_teacher)
        if teacher_info:
            st.caption(f"🎯 **Expertise:** {teacher_info['subject']}")
            st.info(f"💡 {teacher_info['description']}")
        
        if selected_teacher != st.session_state['current_teacher']:
            st.session_state['current_teacher'] = selected_teacher
            
        st.subheader(f"Chat with {selected_teacher}")
        
        chat_container = st.container()
        
        with chat_container:
            # Note: The chat history is stored purely by username and teacher for now
            project_context = f"course:{active_course}|teacher:{selected_teacher}"
            history = get_chat_history(username, project_context)
            for msg in history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    
        prompt = st.chat_input(f"Ask {selected_teacher} a question regarding {active_course}...")
        
        if prompt:
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
                    
                with st.chat_message("assistant"):
                    with st.spinner(f"{selected_teacher} is thinking..."):
                        # We pass the active course to the engine to provide context
                        response = get_ai_response(username, prompt, selected_teacher, active_course=active_course)
                        st.markdown(response)
                        safe_rerun()
                        
        st.divider()
        
        # Display Download Button only if there is a chat history
        if history:
            try:
                from utils.pdf_generator import generate_study_notes
                pdf_bytes = generate_study_notes(username, history)
                st.download_button(
                    label="📥 Download Study Notes (PDF)",
                    data=pdf_bytes,
                    file_name=f"{username}_{active_course}_Notes.pdf".replace(" ", "_"),
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except ModuleNotFoundError as e:
                st.warning(
                    "PDF export isn't available because a dependency is missing. "
                    "Install the missing package and rerun."
                )
                st.caption(f"Details: {e}")
            
        st.divider()
        
        # V3.0 - Hybrid Intelligent Project Builder UI
        st.header("🎓 Intelligent Project Builder")
        st.markdown(f"**Custom Domain Projects** for: **{active_course}**")
        
        with st.spinner("Consulting Domain Expert for Project Ideas..."):
            dynamic_projects_md = generate_dynamic_projects(active_course)
            st.markdown(dynamic_projects_md)
            
            # Simple UI to build from generated projects
            st.markdown("---")
            st.markdown("### 🚀 Ready to Build?")
            proj_to_build = st.text_input("Enter the Project Name from above to start building:", placeholder="e.g., AI-Powered ECG Anomaly Detection Dashboard")
            if st.button("Start Building This Project", type="primary"):
                if proj_to_build:
                    create_user_project(username, active_course, proj_to_build, f"Building {proj_to_build} based on the generated architecture.")
                    st.success(f"Awesome choice! '{proj_to_build}' has been initiated. Switch to the 👨‍💻 AI Project Mentor tab to bring it to life.")
                else:
                    st.warning("Please enter a project name first.")
        
        st.divider()
        st.markdown("### Or build your own Custom Project:")
        custom_idea = st.text_input("Enter your custom project vision:")
        if st.button("Build Custom Project"):
            if custom_idea:
                create_user_project(username, active_course, "Custom Project", custom_idea)
                st.success("Awesome! Switch to the 👨‍💻 AI Project Mentor tab to bring it to life.")
            else:
                st.warning("Please enter an idea first.")

if __name__ == "__main__":
    st.set_page_config(page_title="Student Workspace", page_icon="🎒", layout="wide")
    
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        render_dashboard(st.session_state.get('username', 'Student'))
    else:
        st.sidebar.warning("Running in Test Mode (Not logged in through Auth).")
        render_dashboard("Test_Student")
