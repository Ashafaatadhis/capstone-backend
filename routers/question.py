from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from schemas.question import QuestionCreate, QuestionRead, QuestionUpdate
from services.question_service import QuestionService
from utils.auth import get_current_user
from models.user import User, UserRole
from utils.response import success_response


router = APIRouter(prefix="/questions", tags=["Questions"])


# Public: GET all questions
@router.get("/")
def get_questions(session: Session = Depends(get_session)):
    questions = QuestionService.get_all(session)
    return success_response(data=questions)


# Admin only: Create question
@router.post("/")
def create_question(
    data: QuestionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.admin]:
        raise HTTPException(403, "Unauthorized")

    q = QuestionService.create(session, data)
    return success_response(message="Question created", data=q)


# Admin only: Get question by id
@router.get("/{question_id}")
def get_question(
    question_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    q = QuestionService.get_by_id(session, question_id)
    if not q:
        raise HTTPException(404, "Question not found")
    return success_response(message="Question created", data=q)


# Admin only: Update
@router.put("/{question_id}")
def update_question(
    question_id: int,
    data: QuestionUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    q = QuestionService.update(session, question_id, data)
    if not q:
        raise HTTPException(404, "Question not found")
    return success_response(message="Question updated", data=q)


# Admin only: Delete
@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    success = QuestionService.delete(session, question_id)
    if not success:
        raise HTTPException(404, "Question not found")

    return success_response(message="Deleted successfully", data=None)
