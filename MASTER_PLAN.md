# Project Name: Bharat AI School (V5.0 - Career & Monetization Engine)

## 🎯 TARGET AUDIENCE & CONTEXT
- **Audience:** Hindi-speaking, Tier 2/3 India audiences (ages 18–35).
- **Languages (7):** Hindi, English, Bengali, Tamil, Telugu, Marathi, and Gujarati.
- **Core Differentiator:** A premium, high-trust EdTech platform. NO TOY FEATURES.

## 🚀 CORE VISION: V5.0 Career & Monetization Engine (Outcome-Driven Learning)

### 🛑 V5.0 CORE PRINCIPLES
1. **Outcome-Oriented Courses:** Every course and generated syllabus must clearly state the **Career Benefit**, exactly **WHERE** it will be built (e.g., VS Code, Streamlit, GitHub), and **real-world monetization/utility** (Evidence-based, no overhype).
2. **Interactive Syllabus:** Syllabi are no longer static text. They must be **interactive (expandable modules)**. Clicking a module must explain why it's important and how it applies to the real world.
3. **Deep Project Builder:** The Intelligent Project Builder must stop giving repetitive 1-liners. It must act as a **Startup Advisor**, providing: **The Problem, The Solution, The Tech Stack (Where to build), Publishing Strategy, and Monetization/Career Impact.**

### 🛑 V3.0 STRICT RULE 1 (The Credibility Rule)
ABSOLUTELY NO RANDOM PAID COURSERA LINKS OR WEB PROBING. The course library must only contain genuinely FREE, high-quality, hardcoded curated content (YouTube, DeepLearning.ai free tier, Hugging Face). No random web search that pulls paid spam.

### 🛑 V3.0 STRICT RULE 2 (The Builder Mentor)
The AI Project Mentor must logically act as a 'Full-Stack Builder'. It does not give vague theory or random MCQs. It gives the user real working code, technical architecture, and step-by-step instructions to deploy actual apps.

## 🏛️ THE 10-PILLAR MASTER BLUEPRINT
1. **Dual-Track Curriculum:** Track A: Daily Hacks (general users); Track B: AI Tool Mastery (Beginner → Super Pro).
2. **Duolingo-style Streak + XP:** Gamified engagement system.
3. **Database Auto-Save:** Encrypted backend with user data persistence (State Management).
4. **Digital Certificates + Sharing:** LinkedIn and WhatsApp shareable certificates.
5. **Tech Ki Duniya News Feed:** AI news styled like Instagram Reels.
6. **3-Phase UPI Monetization:** Phase 1: Free → Phase 2: Micro ₹9–49 UPI → Phase 3: ₹99/month via Razorpay.
7. **WhatsApp Community Integration:** Seamless community building.
8. **Deep Project Builder (Pillar 8):** Post-chapter auto-generated projects. Users get 3 options (A. Market problem, B. Another problem, C. Custom blank box). Each option acts as a **Startup Advisor** report (Problem, Solution, Stack, Strategy, Impact).
9. **Project Marketplace (Pillar 9):** App users can showcase, buy, or sell projects (Community Buy, External Submit for commission).
10. **AI Project Mentor Flow (Pillar 10):** A separate guided page (Market research → Problem ID → Build → Launch).

---

## 🧭 V4.0 CORE PILLAR: The Personalized AI Course & Career Guide (Game Changer)

### 🧩 Architecture Overview (End-to-End Loop)

#### 1) User Profiling Input (Sidebar)
A new sidebar feature where the user defines:
- **Identity**: e.g., “5th Grade Student”, “Cardiologist”, “SEO Agency Owner”
- **Goal**: e.g., “Get a job in AI”, “Automate my clinic workflows”, “Grow leads”
- **Preference**: **Free-only resources** vs **Paid/Premium resources allowed**

This becomes the **User Profile** used for personalization across the app.

#### 2) Dynamic & Interactive Syllabus Generation (Groq/LLM)
When the user clicks “Generate My Guide”, the system uses Groq/LLM as a world-class guide to create a:
- **Interactive Syllabus** with expandable modules.
- Each module explains **Career Benefit**, **WHERE** to build, and **Monetization Strategy**.
- Clear outputs (what the user will build/achieve at each step)
- Optional resource mapping based on preference (free-only vs paid-allowed)

The output must be structured and easy to follow (non-coder friendly).

#### 3) The Workflow Loop (Accept → Save → Activate)
After the syllabus is generated:
- user reviews it and clicks **Accept**
- the syllabus is saved to the database as a new **Active Course**
- this course becomes selectable like other courses (and appears in Resume Learning)

#### 4) Mentor Integration (Build Practical Projects from the Custom Syllabus)
Once activated, the user can take this personalized syllabus directly to:
- **Student Study Room** (course chat)
- **AI Project Mentor**

The mentor must read the syllabus and:
- act as a **Startup Advisor** for projects.
- help build them with clear instructions (especially for non-coders)
- keep memory isolated to that specific active course/project context

### 🔐 Data & State Requirements
- Persist **User Profile** in DB (not just session state)
- Persist **Custom Syllabus** as an active course record
- Ensure chat memory and progress are scoped by **username + course/project context**

### ✅ Success Criteria
- user can define profile in sidebar
- user gets a custom syllabus in 1 click
- user accepts it and it becomes an active course
- mentor can use it to build projects step-by-step

## 🛠️ V2.1 FOUNDATION FIXES (PRIORITY ISSUES TO SOLVE)
- **Issue 1: Ultimate AI Course Aggregator:** A centralized directory for third-party courses (ChatGPT, Claude, Gemini, Hugging Face). Categorized by Free/Paid, rated 1 to 5 stars, with new course alerts.
- **Issue 2: Progress Tracking (Resume Learning):** Save user progress in the database. When they return, a "Resume" button takes them exactly to where they left off.
- **Issue 3: Certificate Engine:** Once a course is 100% complete, auto-generate a downloadable certificate.
- **Issue 4: AI Mentor Brain Fix (Anti-Ghajini):** Fix the mentor so it remembers past chats (Persistent Memory), generates dynamic/fresh projects every time (no repetitive projects), and perfectly understands the user's custom project input.

## 💻 CORE STACK
- **UI:** Streamlit
- **Database:** SQLite (Built to scale for Supabase later)

## 📁 FOLDER STRUCTURE
- `app.py`
- `db.py`
- `auth.py`
- `school_workspace.py`
- `ai_teachers.py`
- `engine.py`
- `memory.py`
- `project_mentor.py`
- `admin_panel.py`
- `utils/` (folder including `groq_client.py`, `pdf_generator.py`)

## 📊 CURRENT STATUS
- `db.py` (Completed)
- `auth.py` (Completed)
- `school_workspace.py` (Completed)
- `app.py` (Completed)
- `ai_teachers.py` (Completed)
- `engine.py` (Completed)
- `memory.py` (Completed)
- `utils/groq_client.py` (Completed)
- `admin_panel.py` (Completed)
- `Live Chat Dashboard Setup Complete`

🌟 **Phase 1: Basic UI & DB is 100% Complete!** 🌟
🌟 **Phase 2: AI Brain & Memory is 100% Complete!** 🌟
🌟 **Phase 3: Real AI API Integration & Admin Setup is 100% Complete!** 🌟

🌟 **Phase 4: The Intelligence Upgrade (Reasoning Maps & MCP)** 🌟
AI Mentor uses internal Knowledge Graphs (Nodes & Rules) to force structured reasoning, preventing generic chatbot behavior.
Future Readiness: Preparing the app to use MCP servers (via Claude/Groq) to connect with external tools (GitHub, Twilio, n8n) for real-world execution.

🌟 **Phase 5: Core Profiling, Utilities & Specialization** 🌟
- **User Profiling:** Implementation of 'Non-Coder', 'Beginner', and 'Pro' profiles triggering tailored AI verbosity and chunking.
- **Dynamic Utility:** Trending AI Skills Feed and External URL tracking integration.
- **Sector Specialization:** Specialized standalone environments, starting with the **Doctors AI Hub**, demonstrating a vertical pivot pipeline for specific non-tech users.

## ⏳ NEXT PENDING TASKS
- Build V2.1 Foundation Fixes (Course Aggregator, Progress Tracker, Certificate Engine, Mentor Fix).

## ⚠️ STRICT RULES FOR AI (Antigravity/Claude)
- **Rule 1:** Before starting any new task, silently read this `MASTER_PLAN.md` file and `db.py` to ensure the project rules and context are not forgotten.
- **Rule 2:** (V2.0 Core Law) Before writing any new code or proposing any generic feature, silently verify if it strictly supports the 10-Pillars and the "Career Launchpad" vision. ABSOLUTELY NO TOY FEATURES. Every new feature must contribute to: Learn -> Build -> Market -> Sell.
- **Rule 3:** (Foundation First) Do not build the complex Project Builder UI until the core V2.1 fixes (Memory, Tracking, Certificates) are perfectly stable.
