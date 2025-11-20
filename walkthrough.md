# Grok-CommIT Rebuild Walkthrough

The Grok-CommIT project has been successfully rebuilt from the ground up as a "Cognitive Operating System". The legacy codebase has been archived, and a new full-stack architecture has been implemented.

## 🏗️ New Architecture

The system is now divided into two main components:

### 1. Cognitive Engine (Backend)
- **Path**: `/backend`
- **Tech**: Python, FastAPI, SQLModel (SQLite)
- **Purpose**: Manages the state of the CommIT Cycle, stores projects/messages, and interfaces with LLMs.
- **Key Files**:
    - `main.py`: API entry point and endpoints.
    - `models.py`: Database schema (Project, Cycle, ChatMessage).
    - `engine.py`: State machine logic.
    - `llm.py`: LLM integration service (currently a placeholder).

### 2. Cognitive Cockpit (Frontend)
- **Path**: `/frontend`
- **Tech**: React, Vite, TailwindCSS
- **Purpose**: Provides a visual interface for the CommIT Cycle, chat, and artifact editing.
- **Key Components**:
    - `CycleVisualizer`: Displays the 5 phases (Initiate, Challenge, Implement, Document, Review).
    - `ChatInterface`: "Cyber-Mystic" chat UI.
    - `ArtifactEditor`: Split-pane editor for working documents.

## 🚀 How to Run

### Backend
1. Open a terminal in the project root.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Create a `backend/.env` file from `backend/.env.example`.
4. Configure your `LLM_PROVIDER` in `.env`.
5. Start the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend
1. Open a terminal in the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The UI will be available at `http://localhost:5173`.

## 🎨 Features Implemented

- **Repository Cleanup**: All legacy files moved to `legacy/`.
- **Cyber-Mystic Theme**: Custom Tailwind configuration for a neon/dark aesthetic.
- **Cycle Visualization**: Interactive display of the current thinking phase.
- **Integrated Chat**: Frontend communicates with the Backend API.
- **Persona Injection**: The "CommIT Guide" primer is loaded by the backend.

## 🔮 Next Steps

- **Real LLM Integration**: Uncomment the OpenAI code in `backend/llm.py` and add a valid API key.
- **Guardian Module**: Implement logic in `engine.py` to enforce cycle adherence.
- **File System Access**: Give the AI agentic capabilities to read/write project files directly.
