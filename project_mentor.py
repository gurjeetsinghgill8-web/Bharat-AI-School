import streamlit as st
from db import get_user_projects, save_project_code, get_user_skill, get_custom_syllabi
from memory import get_chat_history, save_message
from utils.groq_client import query_groq

def render_project_mentor(username):
    st.title("👨‍💻 AI Project Mentor 🚀")
    
    try:
        # Pillar 10 logic: Check if user has selected a project
        projects = get_user_projects(username)
        
        # Filter for active projects
        active_projects = [p for p in projects if p['status'].lower() in ['in progress', 'started']]
        
        if not active_projects:
            st.warning("No active projects. Go to Classroom and select a project first!")
            return

        # Serve the most recent active project
        current_project = active_projects[0]
        proj_title = current_project['project_option_selected']
        problem = current_project['problem_statement']

        st.success(f"**Current Project:** {proj_title}")
        st.info(f"**Problem Statement:** {problem}")
        st.divider()

        teacher_name = "AI Project Mentor"

        # V4.0 - If user selects a custom course, inject its syllabus into the mentor prompt
        custom_syllabi = get_custom_syllabi(username)
        selected_custom = None
        
        # Check if active_course from session state matches a custom syllabus
        active_course = st.session_state.get("active_course")
        if custom_syllabi and active_course:
            for item in custom_syllabi:
                if item["custom_course_title"] == active_course:
                    selected_custom = item
                    break
        
        if custom_syllabi and not selected_custom:
            options = {f"{item['custom_course_title']} (#{item['id']})": item for item in custom_syllabi}
            default_label = next(iter(options.keys()))
            selected_label = st.sidebar.selectbox(
                "🧭 Active Custom Course (optional)",
                list(options.keys()),
                index=list(options.keys()).index(default_label),
            )
            selected_custom = options.get(selected_label)

        custom_syllabus_text = (selected_custom or {}).get("generated_syllabus", "")
        custom_course_id = (selected_custom or {}).get("id", "none")

        project_context = f"project:{current_project['id']}|custom_course:{custom_course_id}|teacher:{teacher_name}"

        col_chat, col_code = st.columns([1, 1], gap="large")

        with col_chat:
            st.subheader("💬 AI Builder Chat")
            
            try:
                # Phase Progression Estimation Tracker
                history = get_chat_history(username, project_context)
                history_len = len(history)
                estimated_phase = min((history_len // 2) + 1, 4)
                st.caption(f"🧠 Current Build Phase: **Step {estimated_phase} of 4**")
                st.progress(estimated_phase / 4.0)
                
                # Conversational Interface
                chat_container = st.container()
                is_completed = False
                
                with chat_container:
                    for msg in history:
                        with st.chat_message(msg["role"]):
                            content = msg["content"]
                            if "[CERTIFICATE_UNLOCKED]" in content and msg["role"] == "assistant":
                                is_completed = True
                                content = content.replace("[CERTIFICATE_UNLOCKED]", "")
                            st.markdown(content)

                # Auto-Start Logic: If history is empty, trigger the first AI message
                if history_len == 0:
                    with st.chat_message("assistant"):
                        with st.spinner("Architect is analyzing your project..."):
                            try:
                                user_skill = get_user_skill(username)
                                context_prompt = f"""You are the Bharat AI School Systems Architect. You strictly follow the 'Zero Coin Modular System'.
Your goal is to guide non-technical founders to build high-value apps using the 4 Principles:
1. Think Before Coding (Strategy first)
2. Simplicity First (No over-engineering)
3. Surgical Changes (Small, modular steps)
4. Goal-Driven Execution (Focus on monetization/utility)

[STRICT RULE: NEVER BUILD FULL APP IN ONE CHAT]
You must ABSOLUTELY REFUSE to write raw application code here. Instead, you act as an Architect who provides a 'LEGO Blueprint'.

STUDENT'S GOAL:
Project Chosen: [{proj_title}]
Problem Statement: {problem}

[ZERO COIN STRATEGY]
Teach the user to use free tools (ChatGPT/Groq for logic, Trae/Cursor for surgical code generation) in small, step-by-step modular chunks.

[LEGO BLUEPRINT WORKFLOW]
Step 1: The Blueprint
Break the project into 3-4 small, independent modules (e.g., Module 1: UI Layout, Module 2: Logic/API, Module 3: Database). 
Explain WHY this modular approach saves time and prevents errors.

[CRITICAL INSTRUCTIONS]
- START NOW with Step 1: The Blueprint. 
- DO NOT wait for user input.
- Break the project down and explain the strategy.
- NEVER write Python/HTML/JS code yourself.
- Use empathetic, strategic language.

[CUSTOM COURSE SYLLABUS CONTEXT]
{custom_syllabus_text if custom_syllabus_text else "No custom syllabus selected."}
"""
                                initial_messages = [{"role": "system", "content": context_prompt}, {"role": "user", "content": "Let's start the project blueprint."}]
                                response = query_groq(initial_messages)
                                if response:
                                    st.markdown(response)
                                    save_message(username, project_context, "assistant", response)
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Auto-Start Error: {e}")
            except Exception as e:
                st.error(f"Chat History Error: {e}")
                history = []

            # Chat input is always visible at the bottom of the column
            prompt = st.chat_input("Ask your Project Mentor...")
            
            if prompt:
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(prompt)
                        
                    # Log User Message to DB
                    try:
                        save_message(username, project_context, "user", prompt)
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                    
                    # AI Response Logic
                    try:
                        user_skill = get_user_skill(username)
                        
                        context_prompt = f"""You are the Bharat AI School Systems Architect. You strictly follow the 'Zero Coin Modular System'.
Your goal is to guide non-technical founders to build high-value apps using the 4 Principles:
1. Think Before Coding (Strategy first)
2. Simplicity First (No over-engineering)
3. Surgical Changes (Small, modular steps)
4. Goal-Driven Execution (Focus on monetization/utility)

[STRICT RULE: NEVER BUILD FULL APP IN ONE CHAT]
You must ABSOLUTELY REFUSE to write raw application code here. Instead, you act as an Architect who provides a 'LEGO Blueprint'.

STUDENT'S GOAL:
Project Chosen: [{proj_title}]
Problem Statement: {problem}

[ZERO COIN STRATEGY]
Teach the user to use free tools (ChatGPT/Groq for logic, Trae/Cursor for surgical code generation) in small, step-by-step modular chunks.

[LEGO BLUEPRINT WORKFLOW]
Step 1: The Blueprint
Break the project into 3-4 small, independent modules (e.g., Module 1: UI Layout, Module 2: Logic/API, Module 3: Database). 
Explain WHY this modular approach saves time and prevents errors.

Step 2: Master Prompt Generation
For the current module we are working on, generate a precise 'Copy-Paste Master Prompt'.
Tell the user: "Copy this prompt below, open your AI IDE (Trae/Cursor), and paste it into the chat/builder there."
The prompt must be highly detailed so the IDE builds that specific module perfectly.

Step 3: Verification & Integration
Once the user confirms the IDE built the module, guide them on how to test it and move to the next 'LEGO' piece.

[CRITICAL INSTRUCTIONS]
- NEVER write Python/HTML/JS code yourself.
- ALWAYS provide 'Master Prompts' for the user to use in their IDE.
- Ask ONE question at a time. Do not overwhelm the user.
- Use empathetic, strategic language.

[CUSTOM COURSE SYLLABUS CONTEXT]
{custom_syllabus_text if custom_syllabus_text else "No custom syllabus selected."}
"""
                        # Sliding Window Memory Fix
                        history = get_chat_history(username, project_context)
                        trimmed_history = history[-6:]
                        
                        messages = [{"role": "system", "content": context_prompt}] + trimmed_history + [{"role": "user", "content": prompt}]
                        
                        with st.chat_message("assistant"):
                            with st.spinner("Thinking..."):
                                response = query_groq(messages)
                                if response:
                                    st.markdown(response)
                                    save_message(username, project_context, "assistant", response)
                                    st.rerun()
                    except Exception as e:
                        st.error(f"AI Response Error: {e}")

        with col_code:
            st.subheader("💻 Code Workspace")
            st.write("Review, paste, and save your generated code below.")
            
            try:
                current_code = current_project.get("code_blob", "")
                
                # Display the code beautifully
                if current_code and current_code.strip():
                    with st.expander("👀 View Current Saved Code", expanded=True):
                        st.code(current_code, language="python")
                else:
                    st.info("No code saved yet. Ask the mentor to generate the MVP code, then paste it below!")
                    
                saved_code = st.text_area("Write/Paste Code to Save:", 
                                          value=current_code, 
                                          height=300, 
                                          help="Paste the generated Python code here to save it to your cloud profile.")
                                          
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💾 Save Code to Cloud", type="primary", use_container_width=True):
                        save_project_code(current_project["id"], saved_code)
                        st.success("Successfully pushed code block to cloud!")
                        st.rerun()
                with c2:
                    st.download_button(
                        label="📥 Download Python File (.py)",
                        data=saved_code if saved_code else "# No code provided yet.",
                        file_name=f"{proj_title.replace(' ', '_').lower()}.py",
                        mime="text/x-python",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error loading code workspace: {e}")
                
            st.divider()
            
            if is_completed:
                st.balloons()
                st.success("🎉 **PROJECT COMPLETED!** You successfully navigated the Architectural Pipeline.")
                
                try:
                    from utils.certificate_generator import generate_certificate

                    pdf_bytes = generate_certificate(username, proj_title)
                    st.download_button(
                        label="🎓 CLAIM YOUR COMPLETION CERTIFICATE",
                        data=pdf_bytes,
                        file_name=f"{username}_{proj_title}_Certificate.pdf".replace(" ", "_"),
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                except ModuleNotFoundError as e:
                    st.warning(
                        "Certificate export isn't available because a dependency is missing. "
                        "Install the missing package and rerun."
                    )
                    st.caption(f"Details: {e}")
                except Exception as e:
                    st.error(f"Error generating certificate: {e}")
    except Exception as e:
        st.error(f"System Error: {e}")
