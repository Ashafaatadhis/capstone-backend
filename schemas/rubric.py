from pydantic import BaseModel
from typing import Optional

class RubricCreate(BaseModel):
    score: int
    description: str

class RubricUpdate(BaseModel):
    score: Optional[int] = None
    description: Optional[str] = None

class RubricRead(BaseModel):
    id: int
    question_id: int
    score: int
    description: str
