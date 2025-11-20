from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, create_engine

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    cycles: List["Cycle"] = Relationship(back_populates="project")

class Cycle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    phase: str = Field(default="Initiate") # Initiate, Challenge, Implement, Document, Review
    status: str = Field(default="Active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    project: Project = Relationship(back_populates="cycles")
    messages: List["ChatMessage"] = Relationship(back_populates="cycle")

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cycle_id: int = Field(foreign_key="cycle.id")
    role: str # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    cycle: Cycle = Relationship(back_populates="messages")

# Database Setup
sqlite_file_name = "cognitive_engine.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
