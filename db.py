import os
import streamlit as st
try:
    from supabase import PostgrestError
except ImportError:
    PostgrestError = Exception  # fallback if supabase not installed
# Supabase client import is performed lazily inside get_supabase to avoid ImportError if the package is missing.
# from supabase import create_client, Client  # moved inside function

# Supabase Configuration via st.secrets
# Retrieve Supabase credentials safely.
# Prefer environment variables; if not set, try Streamlit secrets.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    try:
        # Streamlit secrets may raise if not configured
        SUPABASE_URL = st.secrets.get("SUPABASE_URL")
        SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
    except Exception:
        # Keep as None if still not found
        SUPABASE_URL = SUPABASE_URL or None
        SUPABASE_KEY = SUPABASE_KEY or None

@st.cache_resource
def get_supabase():
    """
    Establish and return a connection to the Supabase client.
    Handles missing library and missing credentials gracefully.
    """
    # Lazy import to prevent ImportError at module load time
    try:
        from supabase import create_client, Client
    except ImportError:
        st.error("Supabase Python client is not installed. Run 'pip install supabase' to enable database features.")
        return None

    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("Supabase credentials not found in st.secrets. Please configure them in your Streamlit Cloud dashboard.")
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def _handle_supabase_error(e: Exception, context: str):
    """Handle Supabase errors with specific messages.
    Args:
        e: The caught exception.
        context: Description of the operation (e.g., "Update Skill").
    """
    error_msg = str(e)
    if "PGRST204" in error_msg:
        st.error(
            f"🚨 Supabase schema cache error during {context}: {error_msg}. "
            "Please refresh the Supabase API cache via the dashboard."
        )
    else:
        st.error(f"🚨 Supabase Database Error ({context}): {error_msg}")

def init_db():
    """
    Initializes the Supabase database. 
    Note: In Supabase, you usually create tables via the SQL Editor in the Dashboard.
    I will provide the SQL instructions in the response for you to run once.
    """
    st.info("Supabase migration active. Ensure you have run the required SQL in your Supabase SQL Editor.")

# ==========================================
# V2.0 Helper Data Functions (Project & Marketplace)
# ==========================================

def create_user_project(username: str, course_name: str, project_option_selected: str, problem_statement: str):
    """Insert a newly initiated auto-generated project into Supabase."""
    supabase = get_supabase()
    if not supabase: return None
    
    data = {
        "username": username,
        "course_name": course_name,
        "project_option_selected": project_option_selected,
        "problem_statement": problem_statement,
        "status": "In Progress"
    }
    response = supabase.table("user_projects").insert(data).execute()
    return response.data[0]['id'] if response.data else None

def get_user_projects(username: str = None):
    """Fetch all projects from Supabase."""
    supabase = get_supabase()
    if not supabase: return []
    
    query = supabase.table("user_projects").select("*").order("created_at", desc=True)
    if username:
        query = query.eq("username", username)
    
    response = query.execute()
    return response.data

def save_project_code(project_id: int, code_text: str):
    """Save code block against a user project."""
    supabase = get_supabase()
    if not supabase: return
    
    supabase.table("user_projects").update({"code_blob": code_text}).eq("id", project_id).execute()

def list_project_on_marketplace(project_id: int, username: str, project_title: str, price: float = 0.0):
    """List an existing user project on the marketplace."""
    supabase = get_supabase()
    if not supabase: return None
    
    data = {
        "project_id": project_id,
        "username": username,
        "project_title": project_title,
        "price": price
    }
    response = supabase.table("marketplace").insert(data).execute()
    return response.data[0]['id'] if response.data else None

def get_marketplace_projects():
    """Fetch all listed projects in the marketplace from Supabase."""
    supabase = get_supabase()
    if not supabase: return []
    
    response = supabase.table("marketplace").select("*").order("listed_at", desc=True).execute()
    return response.data

# ==========================================
# V2.1 Helper Data Functions (Progress Tracking)
# ==========================================

def update_user_progress(username: str, course_name: str, completion_percentage: float):
    """Upsert course completion progress for a user in Supabase."""
    supabase = get_supabase()
    if not supabase: return
    
    # Check if exists
    existing = supabase.table("user_progress").select("id").eq("username", username).eq("course_name", course_name).execute()
    
    data = {
        "username": username,
        "course_name": course_name,
        "completion_percentage": completion_percentage
    }
    
    if existing.data:
        supabase.table("user_progress").update(data).eq("id", existing.data[0]['id']).execute()
    else:
        supabase.table("user_progress").insert(data).execute()

def get_user_progress(username: str):
    """Fetch incomplete tracked courses from Supabase."""
    supabase = get_supabase()
    if not supabase: return []
    
    response = supabase.table("user_progress").select("*")\
        .eq("username", username)\
        .lt("completion_percentage", 100)\
        .order("last_accessed", desc=True)\
        .execute()
    return response.data

# ==========================================
# V3.1 Helper Data Functions (Profiling)
# ==========================================

def update_user_skill(username: str, skill_level: str):
    """Update a user's skill level in Supabase."""
    supabase = get_supabase()
    if not supabase:
        return
    try:
        supabase.table("users").update({"skill_level": skill_level}).eq("username", username).execute()
    except PostgrestError as e:
        _handle_supabase_error(e, "Update User Skill")
    except Exception as e:
        _handle_supabase_error(e, "Update User Skill")

def get_user_skill(username: str) -> str:
    """Fetch a user's skill level from Supabase."""
    supabase = get_supabase()
    if not supabase:
        return "Unknown"
    try:
        response = supabase.table("users").select("skill_level").eq("username", username).execute()
        if response.data and response.data[0].get('skill_level'):
            return response.data[0]['skill_level']
    except PostgrestError as e:
        _handle_supabase_error(e, "Get User Skill")
    except Exception as e:
        _handle_supabase_error(e, "Get User Skill")
    return "Unknown"

# ==========================================
# V4.0 Helper Data Functions (Custom Syllabi)
# ==========================================

def save_custom_syllabus(username, profile, title, syllabus):
    """Save a dynamically generated custom course syllabus to Supabase."""
    supabase = get_supabase()
    if not supabase: return None
    
    data = {
        "username": username,
        "profile_description": profile,
        "custom_course_title": title,
        "generated_syllabus": syllabus
    }
    response = supabase.table("custom_syllabi").insert(data).execute()
    return response.data[0]['id'] if response.data else None

def get_custom_syllabi(username):
    """Fetch all custom syllabi from Supabase."""
    supabase = get_supabase()
    if not supabase: return []
    
    response = supabase.table("custom_syllabi").select("*").eq("username", username).order("created_at", desc=True).execute()
    return response.data

supabase = get_supabase()  # Global client for legacy imports
if __name__ == "__main__":
    init_db()
