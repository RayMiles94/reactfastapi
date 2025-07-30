from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

class Note(BaseModel):
    name: str
    note: str =  Field(default="Nothing")


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)

notes = []


@router.get('/')
def read_notes():
    return notes

@router.post('/add')
def add_note(note : Note):
    notes.append(note)
    return {"message": "done"}