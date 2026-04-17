import os
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class ClassroomOrchestrator:
    """Orchestrates dynamic AI classroom dialogues using Google Gemini."""

    @staticmethod
    def generate_classroom_script(topic):
        """
        यह फंक्शन Gemini AI का इस्तेमाल करके टीचर और AI स्टूडेंट्स के बीच की लाइव स्क्रिप्ट बनाता है।
        """
        if not api_key:
            return ClassroomOrchestrator._get_fallback_script(topic)

        # Prompt for Gemini to generate a structured multi-agent script
        prompt = f"""
        Act as a multi-agent AI orchestrator for a medical classroom. 
        Generate a highly engaging, professional classroom debate script about the medical topic: "{topic}".
        
        The script MUST be a JSON list of exactly 5 dictionaries with these keys:
        - "role": Use "assistant" for the Teacher and "user" for Students.
        - "name": Character name (e.g., "Teacher (AI)", "Rahul (AI Student)", "Anjali (AI Student)").
        - "avatar": Use these emojis: 🧑‍🏫 for Teacher, 🙋‍♂️ for Rahul, 🙋‍♀️ for Anjali.
        - "content": Detailed dialogue text in English (but the tone should be encouraging for Hindi-speaking learners).
        
        Flow:
        1. Teacher (assistant) introduces {topic} and its clinical significance.
        2. Rahul (user) asks a doubt about practical application or emergency triage.
        3. Teacher (assistant) explains technically but simply.
        4. Anjali (user) asks about first-line protocols or a specific case detail.
        5. Teacher (assistant) concludes with a key takeaway.
        
        Return ONLY the clean JSON list. Do not include markdown tags or intro/outro text.
        """

        try:
            # Use the faster Flash model for responsiveness (Updated to Gemini 2.0)
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            # Robust parsing of JSON from the response
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
                
            script = json.loads(text)
            return script
            
        except Exception as e:
            # Fallback to the hardcoded engaging script if the API call fails
            return ClassroomOrchestrator._get_fallback_script(topic)

    @staticmethod
    def _get_fallback_script(topic):
        """Engaging fallback script if the AI model is unavailable."""
        if not topic:
            topic = "Heart Failure"
            
        return [
            {
                "role": "assistant", 
                "name": "Teacher (AI)", 
                "avatar": "🧑‍🏫", 
                "content": f"Welcome class! Today we are discussing an important topic: **{topic}**. Let's start with the fundamental concepts. Who can tell me why this is critical?"
            },
            {
                "role": "user", 
                "name": "Rahul (AI Student)", 
                "avatar": "🙋‍♂️", 
                "content": f"Sir, I have a doubt before we begin. How does {topic} directly affect the emergency triage protocol?"
            },
            {
                "role": "assistant", 
                "name": "Teacher (AI)", 
                "avatar": "🧑‍🏫", 
                "content": "Excellent question, Rahul! It is critical because the 'golden hour' dictates patient survival. If we miss the early signs, the mortality rate increases drastically."
            },
            {
                "role": "user", 
                "name": "Anjali (AI Student)", 
                "avatar": "🙋‍♀️", 
                "content": "Adding to what Rahul asked, what are the first-line protocols we must follow as soon as the patient arrives?"
            },
            {
                "role": "assistant", 
                "name": "Teacher (AI)", 
                "avatar": "🧑‍🏫", 
                "content": "Good point, Anjali. The first line protocol includes immediate stabilization of vitals and checking history. Now, let's dive deeper into a clinical case study..."
            }
        ]
