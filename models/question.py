from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .rubric import Rubric
from datetime import datetime

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    rubrics: List["Rubric"] = Relationship(back_populates="question")
