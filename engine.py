"""
AI Communication Engine for Bharat AI School.
Responsible for interacting with LLM models.
"""
from ai_teachers import get_teacher_prompt
from memory import get_chat_history, save_message
from utils.groq_client import query_groq

def get_ai_response(username: str, student_message: str, teacher_name: str, active_course: str = None) -> str:
    """
    Combines the teacher's system prompt with the student's message and chat history
    to generate an AI response using the Groq API.
    """
    # Fetch the system prompt for the specified teacher
    system_prompt = get_teacher_prompt(teacher_name)
    
    if active_course:
        system_prompt += f"\n\nCONTEXT: The user is currently studying the course '{active_course}'. Please prioritize your examples and teachings to be relevant to this domain when appropriate."
    
    project_context = f"course:{active_course or 'global'}|teacher:{teacher_name}"

    # Read past chat history from memory
    history = get_chat_history(username, project_context)
    
    # Save the incoming student message to memory
    save_message(username, project_context, 'user', student_message)
    
    # Construct the messages array for the API call
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": student_message}]
    
    # Call the actual Groq API
    ai_response = query_groq(messages)
    
    # Save the real AI response to memory
    save_message(username, project_context, 'assistant', ai_response)
    
    return ai_response


def generate_personalized_syllabus(user_profile: str, resource_preference: str) -> str:
    """
    Generate a highly structured, step-by-step custom course syllabus using AI.
    Uses a Reasoning Map (Context -> Problem -> Solution -> Impact) for hyper-specific utility.
    """
    system_prompt = (
        "You are a World-Class Career & Tech Guide. Before generating any output, you must follow a strict "
        "Reasoning Chain: (User Context -> Core Problem -> Specific Solution -> Real-World Monetization/Career Impact). "
        "Your mission is to provide deeply researched, highly specific learning paths that lead to real-world "
        "utility. Avoid all generic bullet points and fluff. Career Impact must be a hyper-specific, "
        "evidence-based scenario detailing exactly how the user can apply this skill to their profession."
    )

    user_prompt = f"""
I need a highly structured, step-by-step custom course syllabus for the following profile:
- User Profile: {user_profile}
- Resource Preference: {resource_preference}

Please generate a detailed learning path with 8-10 modules.
Format the output STRICTLY as a series of modules using markdown headers (e.g., ### Module 1: Title).
Under each header, you MUST include:
1. **What you will learn**: (2-3 specific, high-value technical or strategic points)
2. **Actionable Resources**: (Specific search terms or instructions like "Search YouTube for X", "Read documentation for Y", or "Use Z tool to practice").
3. **Career Impact & Monetization Scenario**: (A hyper-specific, evidence-based scenario for the profile: {user_profile}. Exactly how they will use this to save time, earn money, or solve a professional problem).

Make the resources highly specific to the {resource_preference} preference.
Format the output clearly using Markdown headers and bullet points.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Use the existing query_groq function
    return query_groq(messages)

def generate_dynamic_projects(course_title):
    """
    Acts as an Elite Startup Advisor using a Reasoning Chain (Market Gap -> Deep Solution -> Impact).
    """
    system_prompt = (
        "You are an Elite Startup Advisor and Domain Expert AI Product Architect. Before suggesting any project, "
        "you must use a structured Reasoning Chain: (User Context -> Market Gap -> Deep Technical Solution -> Monetization/Career Impact). "
        "Your mission is to transform a student's learning into a real-world high-value asset. "
        "Focus on non-repetitive, innovative project ideas that solve real problems. ZERO fluff."
    )
    
    user_prompt = f"""
I need 3 HYPER-SPECIFIC, highly technical, and innovative project ideas for a student who just finished the course: '{course_title}'.
You MUST act as an Elite Startup Advisor using the Reasoning Chain.

For each project, you MUST use this exact strict structure:

### Project Name & Vision: [Name]
- **Market Gap & Problem**: (A deep analysis of why this project is needed right now in the industry).
- **Where & How to Build (Tech Stack)**: (Must explicitly mention real tools like Cursor IDE, VS Code, Streamlit, GitHub, Python, and specific relevant libraries/APIs).
- **Publishing & Monetization Strategy**: (A concrete, evidence-based plan to launch this to the public and exactly how to profit or gain career leverage from it. NO FAKE HYPE).

Example for an 'AI in Healthcare' course:
### Project Name & Vision: Predictive Patient Readmission Dashboard
- **Market Gap & Problem**: Private clinics currently lose 15% revenue due to unoptimized follow-up schedules.
- **Where & How to Build (Tech Stack)**: Python, Scikit-learn for the model, Cursor IDE for development, Streamlit for the frontend, and GitHub for version control.
- **Publishing & Monetization Strategy**: Deploy on Streamlit Cloud, write a technical case study on LinkedIn, and offer as a customized internal tool for private clinics on a monthly subscription.

Generate 3 such innovative projects for '{course_title}'.
"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    return query_groq(messages)
