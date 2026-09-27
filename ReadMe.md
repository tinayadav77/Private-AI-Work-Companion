**Private AI Work Companion**
   It monitors your computer, not you.

A private-first AI work companion designed to understand a user's digital workspace, reduce distractions, help them find information, remember important tasks, and encourage healthier computer habits.
Unlike traditional assistants that mainly wait for commands, the Private AI Work Companion uses digital context + AI + lightweight system monitoring to provide relevant assistance during the workday.

**Why?**

Modern students and professionals work across multiple applications, files, browser tabs, documents and tasks.
**This often leads to:**
Lost files and information
Forgotten tasks
Context switching
Digital distractions
Long uninterrupted computer sessions
Lack of continuity between interactions

The computer knows what is happening on it — but it doesn't understand when the user is struggling.

**What It Does**
**🎙️ VOICE INTERACTION**

Users can speak naturally to the companion instead of manually typing commands.
The system performs local speech-to-text and identifies the user's intent.

![Voice Interaction and Work Day Activity](<img width="1920" height="1080" alt="Screenshot 2026-09-27 114516" src="https://github.com/user-attachments/assets/2a556ad8-4c1b-41e9-a5db-9cc1d164e853" />)

**🔎 PRIVATE SEMANTIC FILE SEARCH**
Users can ask:
"Find my software engineering notes."

The companion searches the configured local workspace using semantic similarity, rather than relying only on exact keyword matches.
It returns relevant files and their relevance scores.

**📝 Task Memory**
Relevant voice instructions such as:
"Remind me to finish my DBMS assignment."
are converted into persistent tasks.
Normal conversation is not automatically stored as tasks.

![File Search and Task Memory](<img width="1920" height="1080" alt="Screenshot 2026-09-27 114528" src="https://github.com/user-attachments/assets/c364a08a-dcf0-45d3-ba9e-a6fdac5598ea" />)
**💻 Workday Activity**

The companion monitors the currently active foreground application and categorizes usage into areas such as:
Focused Work
Browser
Productivity
Entertainment

It can then provide simple focus and wellbeing indicators.

**🧠 Context-Aware Assistance**

The system combines:
Voice → Intent → Local Data → AI Processing → Useful Action
AI is used where understanding is required, while deterministic system information is handled by normal software logic.


**SYSTEM ARCHITECHTURE**
User
 │
 ├── Voice
 │     ↓
 │  Local Speech AI
 │     ↓
 │  Intent Detection
 │     ↓
 ├── Task Memory ───────→ SQLite
 │
 ├── File Search ────────→ Local Documents
 │                          ↓
 │                     Semantic Search
 │
 └── Activity Monitoring → Active Application
                            ↓
                       Focus / Wellness                             
                          ↓
                      Dashboard

 **Privacy by Design**

Privacy is a core design principle.
Local-first processing where possible
No camera required
No continuous screen recording
Tracks the foreground application, not everything running on the PC
Local files are searched from the configured workspace
Only relevant task information is stored
No cloud AI dependency is required for the current prototype

The companion tracks how you work — without turning your computer into a surveillance system.                 

**TECHNOLOGY STACK**                  
**Component**	                         **Technology**
Backend	                           Python, FastAPI
Frontend	                         HTML, CSS, JavaScript
Speech AI                          Faster-Whisper
Semantic AI	                       Sentence Transformers
Database	                         SQLite
System Monitoring                  Python + psutil / Windows APIs
Document Processing	               PyMuPDF

**Snapdragon & Qualcomm AI Hub**
The solution is designed with Snapdragon-powered HP PCs in mind, where on-device AI can enable responsive and privacy-preserving assistance.
The prototype currently demonstrates the core functionality using local CPU-based AI models.
The next optimization stage is to evaluate and deploy suitable models through Qualcomm AI Hub, targeting Snapdragon hardware acceleration and the available AI compute capabilities of Snapdragon-powered PCs.
This architecture allows AI components to evolve toward Snapdragon-optimized on-device inference without changing the core product concept.

Qualcomm AI Lab
Qualcomm AI Hub

Current Prototype

The prototype currently demonstrates:

✅ Local voice transcription
✅ Intent detection
✅ Voice-based task creation
✅ Semantic local file search
✅ Activity tracking
✅ Focus and wellbeing indicators
✅ Dashboard visualization
✅ Local SQLite memory

Some production features, such as advanced folder permissions, deeper context understanding and Snapdragon NPU optimization, are planned for further development.

**Future Direction**
Snapdragon/NPU-optimized AI inference
Smarter context awareness
User-controlled folder permissions
More intelligent proactive assistance
Improved task and memory management
Additional wellbeing and productivity signals

**PROJECT**
**/Private AI Work Companion/**
It monitors your computer, not you.

Built for the **Snapdragon AI Lab Build & Present Challenge**.
