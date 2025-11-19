#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
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
    update_session_progress,
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

class ConversationTurn(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ActionItem(BaseModel):
    text: str
    completed: bool = False

class SessionUpdateRequest(BaseModel):
    sigil: str
    platform: Optional[str] = "Unknown"
    cycle_phase: Optional[str] = "Initiate"
    emotional_tone: Optional[str] = "Unknown"
    conversation: Optional[List[ConversationTurn]] = []
    action_items: Optional[List[ActionItem]] = []
    cycle_progress: Optional[Dict[str, bool]] = {}
    notes: Optional[str] = ""
    status: Optional[str] = "ACTIVE"
    repo_path: Optional[str] = None

class SessionUpdateResponse(BaseModel):
    success: bool
    message: str
    file: Optional[str] = None

class EvolutionChange(BaseModel):
    file: str
    operation: str  # "replace"
    target: str
    replacement: str

class EvolutionPayload(BaseModel):
    summary: str
    changes: List[EvolutionChange]

class EvolveRequest(BaseModel):
    evolution: EvolutionPayload
    repo_path: Optional[str] = None

class EvolveResponse(BaseModel):
    success: bool
    message: str
    changes_applied: int
    branch_name: Optional[str] = None

def validate_python_syntax(content: str) -> bool:
    """Check if the provided content is valid Python code."""
    try:
        ast.parse(content)
        return True
    except SyntaxError:
        return False

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

@app.post("/session/update", response_model=SessionUpdateResponse)
async def update_session(request: SessionUpdateRequest):
    """Update an existing session with conversation progress"""
    repo_path = Path(request.repo_path) if request.repo_path else DEFAULT_REPO_PATH

    # Convert Pydantic models to dicts for the update function
    session_data = {
        "sigil": request.sigil,
        "platform": request.platform,
        "cycle_phase": request.cycle_phase,
        "emotional_tone": request.emotional_tone,
        "conversation": [turn.dict() for turn in request.conversation] if request.conversation else [],
        "action_items": [item.dict() for item in request.action_items] if request.action_items else [],
        "cycle_progress": request.cycle_progress or {},
        "notes": request.notes or "",
        "status": request.status or "ACTIVE"
    }

    result = update_session_progress(repo_path, request.sigil, session_data, silent=True)

    if result.get("success"):
        return SessionUpdateResponse(
            success=True,
            message=f"Session {request.sigil} updated successfully",
            file=result.get("file")
        )
    else:
        raise HTTPException(status_code=404, detail=result.get("error", "Unknown error"))

@app.post("/evolve", response_model=EvolveResponse)
async def evolve(request: EvolveRequest):
    """Apply self-evolution changes to the codebase in a sandboxed git branch."""
    repo_path = Path(request.repo_path) if request.repo_path else DEFAULT_REPO_PATH
    
    # 1. Check for Git
    if not check_git_availability(silent=True):
        return EvolveResponse(
            success=False,
            message="Git is required for evolution but was not found.",
            changes_applied=0
        )

    # 2. Create Sandboxed Branch
    mutation_id = str(uuid.uuid4())[:8]
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    branch_name = f"mutation/{date_str}-{mutation_id}"
    
    try:
        # Create and checkout new branch
        subprocess.run(["git", "-C", str(repo_path), "checkout", "-b", branch_name], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return EvolveResponse(
            success=False,
            message=f"Failed to create mutation branch: {e}",
            changes_applied=0
        )

    changes_applied = 0
    errors = []

    for change in request.evolution.changes:
        try:
            # Security check: prevent path traversal
            if ".." in change.file or change.file.startswith("/") or "\\" in change.file:
                errors.append(f"Invalid file path: {change.file}")
                continue

            target_file = repo_path / change.file
            
            if not target_file.exists():
                errors.append(f"File not found: {change.file}")
                continue

            content = target_file.read_text(encoding="utf-8")
            new_content = content
            
            if change.operation == "replace":
                if change.target not in content:
                    errors.append(f"Target content not found in {change.file}")
                    continue
                new_content = content.replace(change.target, change.replacement)
            
            # Syntax Validation (The Litmus Test)
            if change.file.endswith(".py"):
                if not validate_python_syntax(new_content):
                    errors.append(f"Syntax Error in {change.file}: The mutation would break the spell.")
                    continue

            # Apply Change
            target_file.write_text(new_content, encoding="utf-8")
            
            # Stage File
            subprocess.run(["git", "-C", str(repo_path), "add", change.file], check=True, capture_output=True)
            changes_applied += 1
                
        except Exception as e:
            errors.append(f"Error processing {change.file}: {str(e)}")

    if changes_applied > 0:
        # Commit the mutation
        commit_msg = f"Mutation: {request.evolution.summary}"
        subprocess.run(["git", "-C", str(repo_path), "commit", "-m", commit_msg], capture_output=True)
        
        message = f"Evolution complete. {changes_applied} mutations applied to branch '{branch_name}'."
        if errors:
            message += f" Errors: {'; '.join(errors)}"
            
        return EvolveResponse(
            success=True,
            message=message,
            changes_applied=changes_applied,
            branch_name=branch_name
        )
    else:
        # Cleanup: Switch back to main and delete empty branch
        subprocess.run(["git", "-C", str(repo_path), "checkout", "-"], capture_output=True)
        subprocess.run(["git", "-C", str(repo_path), "branch", "-D", branch_name], capture_output=True)
        
        return EvolveResponse(
            success=False,
            message=f"No changes applied. Errors: {'; '.join(errors)}",
            changes_applied=0
        )

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
