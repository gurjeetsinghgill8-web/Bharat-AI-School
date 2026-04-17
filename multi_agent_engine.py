class ClassroomOrchestrator:
    """Orchestrates AI classroom dialogues.
    Currently returns a hard‑coded script; later can be swapped for real LLM calls.
    """
    def generate_classroom_script(self, topic: str):
        """Return a list of dialogue turns for a given medical topic.
        Each turn is a dict with keys "role" and "content".
        """
        return [
            {
                "role": "Teacher",
                "content": f"Welcome class, today we discuss {topic}..."
            },
            {
                "role": "AI_Student_Rahul",
                "content": "Sir, I have a doubt regarding the pathophysiology of this condition."
            },
            {
                "role": "Teacher",
                "content": "Great question Rahul, let me explain..."
            }
        ]
