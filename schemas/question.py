from pydantic import BaseModel
from typing import Optional

class QuestionCreate(BaseModel):
    text: str

class QuestionUpdate(BaseModel):
    text: Optional[str] = None

class QuestionRead(BaseModel):
    id: int
    text: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
