from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Optional
from .models import create_db_and_tables
from .llm import LLMService

llm_service = LLMService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Grok-CommIT Cognitive Engine",
    description="The backend for the Cognitive Operating System.",
    version="4.0.0",
    lifespan=lifespan
)

# CORS - Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]

@app.get("/")
async def root():
    return {"message": "The Cognitive Engine is online.", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # Construct full history for LLM
    messages = [{"role": m.role, "content": m.content} for m in request.history]
    messages.append({"role": "user", "content": request.message})
    
    response_content = await llm_service.generate_response(messages)
    
    return {
        "role": "assistant",
        "content": response_content,
        # "phase": "Challenge" # Logic to determine phase would go here
    }
