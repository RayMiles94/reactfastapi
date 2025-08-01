from sqlmodel import SQLModel, create_engine, Session
import os
from .notes.models import *
from .logs.models import *

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://noteuser:user45871A@localhost:5432/notes")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
