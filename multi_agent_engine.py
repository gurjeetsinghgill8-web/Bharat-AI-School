import os
import json
import streamlit as st
from groq import Groq

class ClassroomOrchestrator:
    """Orchestrates dynamic AI classroom dialogues using Groq (Llama 3) at MD/DM Level."""

    @staticmethod
    def generate_classroom_script(topic):
        if not topic:
            topic = "Advanced Heart Failure Management"

        api_key = None
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except:
            pass
            
        if not api_key:
            api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            return [{"role": "assistant", "name": "🚨 System Alert", "avatar": "❌", "content": "**ERROR:** GROQ_API_KEY is missing! Please add it to Streamlit Secrets."}]

        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an advanced Multi-Agent Medical Simulator for postgraduate (MD/DM) doctors.
            The clinical topic is: "{topic}"
            
            Generate a highly technical, deep, and realistic debate between 3 agents:
            1. Dr. Sen (Senior Cardiologist/Professor) - Explains pathophysiology, ACC/AHA/ESC guidelines, and final protocols.
            2. Dr. Rahul (Resident) - Asks complex clinical questions about drug interactions, contraindications, or specific patient profiles.
            3. Dr. Anjali (Chief Resident) - Points out recent clinical trials and rare edge cases.
            
            STRICT RULES:
            - DO NOT use generic phrases like "Welcome class" or "Good question".
            - Jump straight into high-yield clinical discussion.
            - Include exact drug names, dosages, side effects, and trial names.
            
            Create exactly 5 turns of conversation.
            Output ONLY a valid JSON array of objects. Do not include markdown tags.
            
            Format exactly like this:
            [
              {{"role": "assistant", "name": "Dr. Sen (Consultant)", "avatar": "🧑⚕️", "content": "text"}},
              {{"role": "user", "name": "Dr. Rahul (Resident)", "avatar": "👨⚕️", "content": "text"}},
              {{"role": "assistant", "name": "Dr. Sen (Consultant)", "avatar": "🧑⚕️", "content": "text"}},
              {{"role": "user", "name": "Dr. Anjali (Chief Resident)", "avatar": "👩⚕️", "content": "text"}},
              {{"role": "assistant", "name": "Dr. Sen (Consultant)", "avatar": "🧑⚕️", "content": "text"}}
            ]
            """

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a JSON output generator. Output only the requested JSON array."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192",
                temperature=0.5,
            )

            text = chat_completion.choices[0].message.content.strip()
            
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
                
            script = json.loads(text)
            return script
            
        except Exception as e:
            return [{"role": "assistant", "name": "🚨 Groq Engine Error", "avatar": "⚠️", "content": f"Groq API Fail ho gaya: {str(e)}"}]
