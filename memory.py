"""
AI Brain & Memory Module.
Handles saving and retrieving chat histories from Supabase Cloud.
"""
from db import get_supabase

def save_message(username: str, project_context: str, role: str, content: str):
    """
    Saves a single message to Supabase.
    """
    if not username: username = "UnknownUser"
    if not project_context: project_context = "global"
    if role not in ("user", "assistant"): role = "user"
    if content is None: content = ""

    supabase = get_supabase()
    if not supabase: return
    
    data = {
        "username": username,
        "project_context": project_context,
        "role": role,
        "content": content
    }
    supabase.table("chat_history").insert(data).execute()

def get_chat_history(username: str, project_context: str, limit: int = 50) -> list:
    """
    Retrieves the recent chat history between a student and a specific project context from Supabase.
    """
    supabase = get_supabase()
    if not supabase: return []
    
    response = supabase.table("chat_history")\
        .select("role, content")\
        .eq("username", username)\
        .eq("project_context", project_context)\
        .order("id", desc=False)\
        .limit(limit)\
        .execute()
        
    return response.data
