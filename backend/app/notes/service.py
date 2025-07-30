from datetime import datetime
from sqlmodel import Session, select
from .models import Note, NoteCreate

def create_note(session: Session, node_data: NoteCreate) -> Note:
    note = Note.from_orm(node_data)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

def get_notes(session: Session):
    return session.exec(select(Note)).all()

def get_note(session: Session, note_id: int):
    return session.get(Note, note_id)

def update_note(session: Session, note_id: int, note_data: NoteCreate):
    note = session.get(Note, note_id)
    if not note:
        return None
    note.name = note_data.name
    note.node = note_data.node
    note.editdate = datetime.utcnow()
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

def delete_note(session: Session, note_id: int):
    note = session.get(Note, note_id)
    if not note:
        return None
    session.delete(note)
    session.commit()
    return note
