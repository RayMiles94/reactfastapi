from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import Text, Integer

class Userbase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user: str = Field(sa_column=Text)
    password: str = Field(sa_column=Text)
    age: int = Field(sa_column=Integer)
    phone : str = Field(sa_column=Text)


class User(Userbase, table=True):
    createdate: datetime = Field(default_factory=datetime.utcnow) 
    updatedate: datetime = Field(default_factory=datetime.utcnow)
