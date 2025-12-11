from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from schemas.user import UserRead
from schemas.auth import LoginRequest, TokenResponse
from models.user import User
from utils.response import ResponseModel
from utils.password import verify_password
from utils.auth import  get_current_user
from utils.jwt import create_access_token, create_refresh_token
from database import get_session


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    stmt = select(User).where(User.username == data.username)
    user = session.exec(stmt).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.id, "role": user.role, "username": user.username})
    refresh_token = create_refresh_token({"sub": user.id, "role": user.role, "username": user.username})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
 

@router.get("/me", response_model=ResponseModel[UserRead])
def get_me(current_user: User = Depends(get_current_user)):
    return ResponseModel(data=current_user)
