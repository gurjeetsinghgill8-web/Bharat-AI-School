"""
Massive Course Catalog Database (V3.0 Mega Fix).
Contains highly structured official certificates and courses.
Each course holds 5 "Gold Standard" projects.
"""

CURATED_COURSES = [
    # ---------------- ANTHROPIC (CLAUDE) ---------------- #
    {
        "id": "anthropic_1",
        "title": "Claude 101",
        "description": "Foundational introduction to the Claude AI ecosystem and best practices.",
        "provider": "Anthropic",
        "level": "Beginner",
        "is_free": True,
        "url": "https://learn.anthropic.com/",
        "career_benefit": "Master the world's most sophisticated reasoning model to automate complex office tasks and research.",
        "tech_stack": "Claude.ai, Anthropic Console, Prompt Engineering",
        "projects": [
            "Claude Prompting Template Tool",
            "Simple Claude Q&A Bot",
            "Text Summarization Dashboard",
            "Idea Validator Assistant",
            "Email Auto-Reply Drafter"
        ]
    },
    {
        "id": "anthropic_2",
        "title": "Introduction to Claude Cowork",
        "description": "Learn how to use Claude to accelerate team workflows and brainstorming.",
        "provider": "Anthropic",
        "level": "Beginner",
        "is_free": True,
        "url": "https://learn.anthropic.com/",
        "career_benefit": "Become an AI-First Team Lead by integrating collaborative AI into sprint planning and corporate comms.",
        "tech_stack": "Claude Projects, Artifacts, Team Workspaces",
        "projects": [
            "Team Ideation Collaborator",
            "Meeting Notes Action Item Extractor",
            "Drafting Corporate Communications",
            "Sprint Planning Companion",
            "HR Policy Document Q&A"
        ]
    },
    {
        "id": "anthropic_3",
        "title": "Building with the Claude API",
        "description": "Advanced API integration, streaming, and function calling workflows.",
        "provider": "Anthropic",
        "level": "Advanced",
        "is_free": True,
        "url": "https://docs.anthropic.com/claude/docs",
        "career_benefit": "Qualify for high-paying AI Engineer roles by building scalable, production-ready AI applications.",
        "tech_stack": "Python, Anthropic SDK, Streamlit, GitHub",
        "projects": [
            "Claude API Streaming CLI",
            "Automated Ticket Triage System",
            "Multi-step Document Parser",
            "Sentiment-Driven Router",
            "Automated Code Refactorer"
        ]
    },
    {
        "id": "anthropic_4",
        "title": "Introduction to Model Context Protocol (MCP)",
        "description": "Mastering long-context data ingestion and contextual memory scaling.",
        "provider": "Anthropic",
        "level": "Advanced",
        "is_free": True,
        "url": "https://docs.anthropic.com/",
        "projects": [
            "MCP Powered Research Assistant",
            "Legal Contract Reviewer Tool",
            "Enterprise Vector Search RAG",
            "PDF Textbook Concept Extractor",
            "Financial Statement Analyzer"
        ]
    },
    {
        "id": "anthropic_5",
        "title": "AI Fluency: Framework & Foundations",
        "description": "The strategic framework for deploying AI across enterprise environments.",
        "provider": "Anthropic",
        "level": "Intermediate",
        "is_free": True,
        "url": "https://learn.anthropic.com/",
        "projects": [
            "AI Adoption Strategy Dashboard",
            "Prompt Library Manager",
            "AI Sandbox Playground",
            "Ethics & Bias Evaluator",
            "Department Tool Recommender"
        ]
    },
    {
        "id": "anthropic_6",
        "title": "Claude Code in Action",
        "description": "Hands-on coding paradigms generating complex logic using Claude 3.",
        "provider": "Anthropic",
        "level": "Advanced",
        "is_free": True,
        "url": "https://docs.anthropic.com/",
        "projects": [
            "Claude Guided Code Reviewer",
            "Unit Test Generator System",
            "Legacy Code Translator",
            "CI/CD Build Error Debugger",
            "SQL Query Optimizer Agent"
        ]
    },

    # ---------------- OPENAI (CHATGPT) ---------------- #
    {
        "id": "openai_1",
        "title": "ChatGPT Prompt Engineering for Developers",
        "description": "Crucial prompt engineering principles taught by OpenAI engineers.",
        "provider": "OpenAI / DeepLearning.AI",
        "level": "Beginner",
        "is_free": True,
        "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/",
        "career_benefit": "Qualify for AI-heavy roles by mastering data extraction, summarization, and tone transformation using LLMs.",
        "tech_stack": "Python, OpenAI API, Streamlit",
        "projects": [
            "Sentiment Analysis Classifier",
            "Automated Email Responder",
            "JSON Data Extractor Tool",
            "Tone Adjusting Markdown Editor",
            "Support Ticket Categorizer"
        ]
    },
    {
        "id": "openai_2",
        "title": "Building Systems with the ChatGPT API",
        "description": "Chaining LLM calls, evaluating outputs, and building secure apps.",
        "provider": "OpenAI / DeepLearning.AI",
        "level": "Intermediate",
        "is_free": True,
        "url": "https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/",
        "career_benefit": "Build robust AI systems that can automate multi-step workflows for customer support and complex data pipelines.",
        "tech_stack": "Python, OpenAI API, Vector Databases (Pinecone/Chroma)",
        "projects": [
            "Multi-Step Customer Support Agent",
            "Fact-Checking Pipeline System",
            "Personalized Content Recommender",
            "Audio/Transcript Pipeline",
            "Roleplaying Negotiation Simulator"
        ]
    },
    {
        "id": "openai_3",
        "title": "Generative AI for Everyone",
        "description": "The non-technical perspective on ChatGPT integration and usage.",
        "provider": "DeepLearning.AI",
        "level": "Beginner",
        "is_free": True,
        "url": "https://www.deeplearning.ai/courses/generative-ai-for-everyone/",
        "career_benefit": "Future-proof your career in any field by understanding how to leverage AI for daily productivity and strategic planning.",
        "tech_stack": "ChatGPT, Bing Chat, Google Gemini",
        "projects": [
            "AI Use-Case Tracker",
            "Productivity Automator Dashboard",
            "Simple Copywriting Assistant",
            "Personal Spending Categorizer",
            "Weekly Menu Planner Bot"
        ]
    },

    # ---------------- GOOGLE (GEMINI) ---------------- #
    {
        "id": "google_1",
        "title": "Introduction to Generative AI",
        "description": "Google Cloud's fundamental primer on Generative AI principles.",
        "provider": "Google",
        "level": "Beginner",
        "is_free": True,
        "url": "https://cloud.google.com/training/generative-ai",
        "career_benefit": "Understand the core of Google's AI technology and how it's used in Enterprise Cloud environments.",
        "tech_stack": "Google Cloud Platform (GCP), Vertex AI, Gemini",
        "projects": [
            "Generative AI Concept Explainer",
            "Gemini Image Prompt Generator",
            "AI Glossary Dashboard",
            "Cloud Service Matchmaker",
            "Visual Flowchart Text Generator"
        ]
    },
    {
        "id": "google_2",
        "title": "Gemini for Google Workspace",
        "description": "Accelerating productivity directly within Google Docs, Sheets, and Mail.",
        "provider": "Google",
        "level": "Beginner",
        "is_free": True,
        "url": "https://workspace.google.com/solutions/ai/",
        "career_benefit": "Become a Google Workspace power user by automating documents, emails, and complex spreadsheet tasks with AI.",
        "tech_stack": "Google Docs, Google Sheets, Google Mail, App Script",
        "projects": [
            "Google Sheets Automated Macro AI",
            "Gmail Intelligent Draft Hub",
            "Workspace Slide Outline Generator",
            "Meeting Calendar RSVP Bot",
            "Google Drive Document Organizer"
        ]
    }
]
