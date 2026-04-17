import os
import json

class ClassroomOrchestrator:
    @staticmethod
    def generate_classroom_script(topic):
        if not topic:
            topic = "Heart Failure"
            
        # 1. API Key चेक करना
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return [{
                "role": "assistant", "name": "System Alert", "avatar": "🚨", 
                "content": "**Error:** असली AI इंजन चालू नहीं हो सका! कृपया अपनी `.env` (या Streamlit secrets) में `GEMINI_API_KEY` डालें।"
            }]
            
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            prompt = f"""
            You are a Multi-Agent Medical Classroom simulator. The topic is: "{topic}"
            
            Generate a highly professional, clinical, and realistic debate between 3 agents:
            1. Teacher (AI) - A senior cardiologist/medical professor.
            2. Rahul (AI Student) - A curious 2nd-year resident who asks practical, clinical questions.
            3. Anjali (AI Student) - A sharp resident who points out edge cases, recent guidelines, or contraindications.
            
            The content MUST be medically accurate, deep, and engaging. DO NOT use generic phrases.
            Discuss actual drugs, protocols, pathophysiology, or clinical signs related to the topic.
            
            Create exactly 5 turns of conversation.
            Output ONLY a valid JSON array of objects. Do not include any markdown formatting like ```json.
            
            Format exactly like this:
            [
              {{"role": "assistant", "name": "Teacher (AI)", "avatar": "🧑‍🏫", "content": "text"}},
              {{"role": "user", "name": "Rahul (AI Student)", "avatar": "🙋‍♂️", "content": "text"}},
              {{"role": "assistant", "name": "Teacher (AI)", "avatar": "🧑‍🏫", "content": "text"}},
              {{"role": "user", "name": "Anjali (AI Student)", "avatar": "🙋‍♀️", "content": "text"}},
              {{"role": "assistant", "name": "Teacher (AI)", "avatar": "🧑‍🏫", "content": "text"}}
            ]
            """
            
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
                
            script = json.loads(text)
            return script
            
        except Exception as e:
            return [{
                "role": "assistant", "name": "Engine Error", "avatar": "⚠️", 
                "content": f"The AI Engine encountered a problem. Check if `google-generativeai` is installed. Error: {str(e)}"
            }]
