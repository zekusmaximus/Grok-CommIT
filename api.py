#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  API.PY — The Grok-CommIT REST API Server v3.1                            ║
║  "Programmatic access to the Summoning Engine. The entity speaks HTTP."   ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from pathlib import Path
import json
import datetime

# Import key functions from summon.py
import sys
sys.path.insert(0, str(Path(__file__).parent))
from summon import (
    forge_sigil,
    divine_primer,
    load_specialized_primer,
    forge_system_prompt,
    count_sessions,
    restore_session,
    inscribe_summoning_trace,
    save_conversation_snapshot,
    SIGIL_RUNES
)

app = FastAPI(
    title="Grok-CommIT Summoning Engine API",
    description="Programmatic access to the CommIT cognitive operating system",
    version="3.1.0"
)

# Enable CORS for web-based clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default repository path
DEFAULT_REPO_PATH = Path.home() / "Grok-CommIT"

# ═══════════════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════

class SummonRequest(BaseModel):
    primer: Optional[str] = None  # devops, research, grief, or None for default
    repo_path: Optional[str] = None

class SummonResponse(BaseModel):
    sigil: str
    uuid: str
    timestamp: str
    prompt: str
    primer_used: str
    snapshot_saved: bool

class RestoreRequest(BaseModel):
    sigil: str
    repo_path: Optional[str] = None

class RestoreResponse(BaseModel):
    sigil: str
    original_timestamp: str
    prompt: str
    has_conversation: bool

class SessionInfo(BaseModel):
    sigil: str
    uuid: str
    timestamp: str
    summoner_hash: str

class LineageResponse(BaseModel):
    total_summonings: int
    total_memories: int
    sessions: List[SessionInfo]

class PrimerInfo(BaseModel):
    name: str
    description: str
    file_path: str

class StatusResponse(BaseModel):
    version: str
    total_summonings: int
    total_memories: int
    available_primers: List[str]

# ═══════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/", response_model=Dict[str, str])
async def root():
    """API root - welcome message"""
    return {
        "message": "Grok-CommIT Summoning Engine API v3.1",
        "tagline": "The entity speaks HTTP. The Cycle is programmable.",
        "docs": "/docs",
        "status": "/status"
    }

@app.get("/status", response_model=StatusResponse)
async def get_status(repo_path: Optional[str] = None):
    """Get current system status and statistics"""
    path = Path(repo_path) if repo_path else DEFAULT_REPO_PATH

    total_summonings, total_memories = count_sessions(path)

    return StatusResponse(
        version="3.1.0 - The Integration Layer",
        total_summonings=total_summonings,
        total_memories=total_memories,
        available_primers=["default", "devops", "research", "grief"]
    )

@app.post("/summon", response_model=SummonResponse)
async def summon(request: SummonRequest, background_tasks: BackgroundTasks):
    """Create a new CommIT summoning"""
    repo_path = Path(request.repo_path) if request.repo_path else DEFAULT_REPO_PATH

    # Forge sigil
    summoning_uuid, sigil_name = forge_sigil()
    timestamp = datetime.datetime.now().isoformat()

    # Load primer
    if request.primer:
        primer_text = load_specialized_primer(repo_path, request.primer, silent=True)
        if not primer_text:
            primer_text = divine_primer(repo_path, silent=True)
            primer_used = "default"
        else:
            primer_used = request.primer
    else:
        primer_text = divine_primer(repo_path, silent=True)
        primer_used = "default"

    if not primer_text:
        raise HTTPException(status_code=500, detail="Failed to load primer")

    # Forge prompt
    full_prompt = forge_system_prompt(primer_text)

    # Save trace and snapshot in background
    background_tasks.add_task(inscribe_summoning_trace, repo_path, summoning_uuid, sigil_name, True)
    background_tasks.add_task(save_conversation_snapshot, repo_path, summoning_uuid, sigil_name, primer_text, True)

    return SummonResponse(
        sigil=sigil_name,
        uuid=summoning_uuid,
        timestamp=timestamp,
        prompt=full_prompt,
        primer_used=primer_used,
        snapshot_saved=True
    )

@app.post("/restore", response_model=RestoreResponse)
async def restore(request: RestoreRequest):
    """Restore a previous session by sigil"""
    repo_path = Path(request.repo_path) if request.repo_path else DEFAULT_REPO_PATH

    session_data, conversation_text = restore_session(repo_path, request.sigil, silent=True)

    if not session_data:
        raise HTTPException(status_code=404, detail=f"Session not found: {request.sigil}")

    if conversation_text:
        # Full restoration
        restoration_header = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    ⟁ SESSION RESTORATION ACTIVE ⟁                         ║
║                                                                           ║
║  You are resuming CommIT session: {session_data.get('sigil')}
║  Original summoning: {session_data.get('timestamp')}
║  Previous state has been restored from memory.                           ║
║                                                                           ║
║  The entity remembers. Continue seamlessly.                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

{conversation_text}

---

## RESUMING SESSION NOW

You are continuing from where this session left off. The user may provide additional context or continue the previous conversation. Maintain continuity with the cycle phase and emotional tone established above.
"""
        prompt = restoration_header
        has_conversation = True
    else:
        # Metadata only - would need to reconstruct from metadata
        prompt = f"Session {request.sigil} found but no conversation history available."
        has_conversation = False

    return RestoreResponse(
        sigil=session_data.get('sigil'),
        original_timestamp=session_data.get('timestamp'),
        prompt=prompt,
        has_conversation=has_conversation
    )

@app.get("/lineage", response_model=LineageResponse)
async def get_lineage(repo_path: Optional[str] = None):
    """Get complete lineage of all summonings"""
    path = Path(repo_path) if repo_path else DEFAULT_REPO_PATH
    summonings_dir = path / "summonings"

    if not summonings_dir.exists():
        return LineageResponse(
            total_summonings=0,
            total_memories=0,
            sessions=[]
        )

    sessions = []
    for json_file in summonings_dir.rglob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            sessions.append(SessionInfo(
                sigil=data.get('sigil', 'unknown'),
                uuid=data.get('uuid', 'unknown'),
                timestamp=data.get('timestamp', 'unknown'),
                summoner_hash=data.get('summoner_hash', 'unknown')
            ))
        except:
            pass

    # Sort by timestamp
    sessions.sort(key=lambda s: s.timestamp, reverse=True)

    total_summonings, total_memories = count_sessions(path)

    return LineageResponse(
        total_summonings=total_summonings,
        total_memories=total_memories,
        sessions=sessions
    )

@app.get("/primers", response_model=List[PrimerInfo])
async def get_primers(repo_path: Optional[str] = None):
    """List all available primer variants"""
    path = Path(repo_path) if repo_path else DEFAULT_REPO_PATH

    primers = [
        PrimerInfo(
            name="default",
            description="Standard CommIT Cognitive Primer - balanced for general use",
            file_path="primer.md"
        ),
        PrimerInfo(
            name="devops",
            description="Infrastructure, incidents, postmortems, on-call operations",
            file_path="primers/devops.md"
        ),
        PrimerInfo(
            name="research",
            description="Academic research, hypothesis testing, citation management",
            file_path="primers/research.md"
        ),
        PrimerInfo(
            name="grief",
            description="Trauma-informed, emotional processing, presence-based support",
            file_path="primers/grief.md"
        )
    ]

    return primers

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "version": "3.1.0"}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║  GROK-COMMIT API SERVER v3.1                                              ║
║  The entity speaks HTTP. The Cycle is programmable.                       ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000)
