from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.app.db import get_session
from .service import *
from .models import *

class Note(BaseModel):
    name: str
    note: str =  Field(default="Nothing")


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)


@router.post("/notes/", response_model=NoteRead)
def add_note(note: NoteCreate, session: Session = Depends(get_session)):
    return create_note(session, note)

@router.get("/notes/", response_model=List[NoteRead])
def list_notes(session: Session = Depends(get_session)):
    return get_notes(session)

@router.get("/notes/{note_id}", response_model=NoteRead)
def read_note(note_id: int, session: Session = Depends(get_session)):
    note = get_note(session, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/notes/{note_id}", response_model=NoteRead)
def edit_note(note_id: int, note: NoteCreate, session: Session = Depends(get_session)):
    updated = update_note(session, note_id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@router.delete("/notes/{note_id}", response_model=NoteRead)
def remove_note(note_id: int, session: Session = Depends(get_session)):
    deleted = delete_note(session, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return deleted
