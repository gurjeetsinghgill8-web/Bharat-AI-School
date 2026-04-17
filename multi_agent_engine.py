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
            You are the core Multi-Agent Simulator for "Bharat AI School". The current year is 2026.
            The learning topic entered by the user is: "{topic}"
            
            CRITICAL INSTRUCTION: You MUST adapt to become a world-class expert in WHATEVER field the topic belongs to (e.g., Programming, AI, Marketing, Science, Medical). You MUST base your discussion on the ABSOLUTE LATEST industry standards, frameworks, tools, and data available in 2025/2026.
            
            Generate a highly engaging, deep, and realistic debate between 3 agents:
            1. Professor AI (Lead Expert) - Explains core concepts and the absolute latest 2026 trends, updates, or paradigms in this specific field.
            2. Rahul (Curious Learner) - Asks practical, real-world execution questions or common beginner/intermediate doubts.
            3. Anjali (Advanced Learner) - Points out edge cases, latest 2026 updates, critical challenges, or future scope.
            
            STRICT RULES:
            - Jump straight into high-yield, cutting-edge discussion.
            - If the topic is Tech/AI, mention latest models/frameworks. If Business, mention current market trends. If Medical, latest guidelines.
            - Be specific, technical, and accurate. No generic fluff.
            
            Create exactly 5 turns of conversation.
            Output ONLY a valid JSON array of objects. Do not include markdown tags.
            
            Format exactly like this:
            [
              {{"role": "assistant", "name": "Professor AI", "avatar": "🧑🏫", "content": "text"}},
              {{"role": "user", "name": "Rahul (Learner)", "avatar": "🙋♂️", "content": "text"}},
              {{"role": "assistant", "name": "Professor AI", "avatar": "🧑🏫", "content": "text"}},
              {{"role": "user", "name": "Anjali (Advanced Learner)", "avatar": "🙋♀️", "content": "text"}},
              {{"role": "assistant", "name": "Professor AI", "avatar": "🧑🏫", "content": "text"}}
            ]
            """

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a JSON output generator. Output only the requested JSON array."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
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
