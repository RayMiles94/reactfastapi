from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Text

class NoteBase(SQLModel):
    name: str
    node: str = Field(sa_column=Text)

class Note(NoteBase, table=True):
    id : Optional[int] = Field(default=None, primary_key=True, index=True)
    createdate: datetime = Field(default_factory=datetime.utcnow) 
    updatedate: datetime = Field(default_factory=datetime.utcnow)

class NoteCreate(NoteBase):
    pass 

class NoteRead(NoteBase):
    id: int
    createdate: datetime = Field(default_factory=datetime.utcnow) 
    updatedate: datetime = Field(default_factory=datetime.utcnow)
