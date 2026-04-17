"""
Groq API Client.
Handles communication with the Groq LLM API.
"""
import os
try:
    from groq import Groq
except ImportError:
    # Just in case groq is not installed, fail gracefully initially
    Groq = None

def query_groq(messages: list) -> str:
    """
    Sends a list of messages to the Groq API and returns the response string.
    """
    if Groq is None:
        return "Error: The 'groq' python library is not installed. Please run 'pip install groq'."

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY environment variable is not set."
        
    client = Groq(api_key=api_key)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",  # Fast and robust default model on Groq
            temperature=0.7,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"
