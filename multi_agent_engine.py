import time

class ClassroomOrchestrator:
    @staticmethod
    def generate_classroom_script(topic):
        """
        यह फंक्शन टीचर और AI स्टूडेंट्स के बीच की लाइव स्क्रिप्ट बनाता है।
        """
        if not topic:
            topic = "General Medicine"
            
        script = [
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
        return script
