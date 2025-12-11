from pydantic import BaseModel
from typing import Optional
from models.user import UserRole


class UserCreate(BaseModel):
    username: str
    password: str   # plaintext, akan di-hash sebelum simpan
    role: UserRole = UserRole.admin


class UserRead(BaseModel):
    id: int
    username: str
    role: UserRole


