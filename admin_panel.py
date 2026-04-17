import streamlit as st
import pandas as pd
from db import get_supabase

def render_admin_dashboard():
    st.title("Admin Dashboard ⚙️")
    st.markdown("Overview and monitoring of the Bharat AI School Platform.")
    
    supabase = get_supabase()
    if not supabase:
        st.error("Supabase connection failed.")
        return

    try:
        # 1. Total Registered Students
        response = supabase.table("users").select("id", count="exact").eq("role", "student").execute()
        total_students = response.count if response.count is not None else 0
        
        # 2. Total Chats
        chat_response = supabase.table("chat_history").select("id", count="exact").execute()
        total_chats = chat_response.count if chat_response.count is not None else 0
        
        # 3. Most Popular AI Teacher (Simulated via project_context parsing if needed, but let's keep it simple for now)
        # Note: In Supabase/SQL, this would be a more complex query. 
        # For now, let's just fetch recent chats and display them.
        most_popular = "AI Project Mentor" # Default for now
        
    except Exception as e:
        st.error(f"Error fetching admin stats: {e}")
        total_students = 0
        total_chats = 0
        most_popular = "N/A"
        
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Total Chat Messages", total_chats)
    col3.metric("Most Popular Teacher", most_popular)
    
    st.divider()
    
    # 4. Recent Chat Logs
    st.subheader("Recent Chat Logs")
    try:
        logs_response = supabase.table("chat_history")\
            .select("username, role, content, created_at")\
            .order("created_at", desc=True)\
            .limit(50)\
            .execute()
            
        if logs_response.data:
            logs_df = pd.DataFrame(logs_response.data)
            st.dataframe(logs_df, use_container_width=True, hide_index=True)
        else:
            st.info("No chat logs available yet.")
    except Exception as e:
        st.error(f"Error fetching logs: {e}")
