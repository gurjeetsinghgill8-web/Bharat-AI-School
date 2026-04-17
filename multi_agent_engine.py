import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClassroomOrchestrator:
    """Orchestrates dynamic AI classroom dialogues using Google Gemini at MD/DM Level."""

    @staticmethod
    def generate_classroom_script(topic):
        if not topic:
            topic = "Advanced Heart Failure Management"

        # 1. API Key को सुरक्षित तरीके से निकालना (बिना क्रैश किए)
        api_key = None
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except:
            pass
            
        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")

        # अगर चाबी नहीं मिली, तो खिलौना मत दिखाओ, सीधा एरर दिखाओ!
        if not api_key:
            return [{
                "role": "assistant", "name": "🚨 System Alert", "avatar": "❌", 
                "content": "**ERROR:** GEMINI_API_KEY नहीं मिली है! कृपया Streamlit Secrets में चाबी डालें।"
            }]

        # 2. असली AI इंजन (Cardiology Level)
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            prompt = f"""
            You are an advanced Multi-Agent Medical Simulator for postgraduate (MD) doctors.
            The clinical topic is: "{topic}"
            
            Generate a highly technical, deep, and realistic debate between 3 agents:
            1. Dr. Sen (Senior Cardiologist/Professor) - Explains pathophysiology, ACC/AHA/ESC guidelines, and final protocols.
            2. Dr. Rahul (Resident) - Asks complex clinical questions about drug interactions, contraindications, or specific patient profiles (e.g., hypotension, renal failure).
            3. Dr. Anjali (Chief Resident) - Points out recent clinical trials (like PARADIGM-HF, DAPA-HF, etc.) and rare edge cases.
            
            STRICT RULES:
            - DO NOT use generic phrases like "Welcome class", "Good question", or "Let's dive in".
            - Jump straight into high-yield clinical discussion.
            - Include exact drug names, dosages, side effects, and trial names.
            - Make it sound like a real ICU or OPD case discussion.
            
            Create exactly 5 turns of conversation.
            Output ONLY a valid JSON array of objects. Do not include markdown tags like ```json.
            
            Format exactly like this:
            [
              {{"role": "assistant", "name": "Dr. Sen (Consultant)", "avatar": "🧑⚕️", "content": "text"}},
              {{"role": "user", "name": "Dr. Rahul (Resident)", "avatar": "👨⚕️", "content": "text"}},
              {{"role": "assistant", "name": "Dr. Sen (Consultant)", "avatar": "🧑⚕️", "content": "text"}},
              {{"role": "user", "name": "Dr. Anjali (Chief Resident)", "avatar": "👩⚕️", "content": "text"}},
              {{"role": "assistant", "name": "Dr. Sen (Consultant)", "avatar": "🧑⚕️", "content": "text"}}
            ]
            """

            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # JSON को पार्स करना
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
                
            script = json.loads(text)
            return script
            
        except Exception as e:
            # अगर AI फेल हो जाए, तो टॉय स्क्रिप्ट नहीं, बल्कि असली एरर दिखाओ!
            return [{
                "role": "assistant", "name": "🚨 AI Engine Error", "avatar": "⚠️", 
                "content": f"AI Engine fail ho gaya: {str(e)}"
            }]
