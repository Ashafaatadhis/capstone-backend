from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from schemas.rubric import RubricCreate, RubricUpdate, RubricRead
from services.rubric_service import RubricService
from services.question_service import QuestionService
from utils.auth import get_current_user
from models.user import User, UserRole
from utils.response import success_response

router = APIRouter(prefix="/rubrics", tags=["Rubrics"])


# Public: get rubrics for a question
@router.get("/question/{question_id}")
def get_rubrics(question_id: int, session: Session = Depends(get_session)):
    q = QuestionService.get_by_id(session, question_id)
    if not q:
        raise HTTPException(404, "Question not found")

    rub = RubricService.get_by_question(session, question_id)
    return success_response(data=rub, message="Rubrics fetched")

# Public/Admin: get rubric by ID
@router.get("/{rubric_id}")
def get_rubric_by_id(
    rubric_id: int,
    session: Session = Depends(get_session),
):
    rub = RubricService.get_by_id(session, rubric_id)
    if not rub:
        raise HTTPException(404, "Rubric not found")

    return success_response(data=rub, message="Rubric fetched")


# Admin: create rubric
@router.post("/question/{question_id}")
def create_rubric(
    question_id: int,
    data: RubricCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.admin]:
        raise HTTPException(403, "Unauthorized")

    q = QuestionService.get_by_id(session, question_id)
    if not q:
        raise HTTPException(404, "Question not found")

    rub = RubricService.create(session, question_id, data)
    return success_response(data=rub, message="Rubric created")


# Admin: update rubric
@router.put("/{rubric_id}")
def update_rubric(
    rubric_id: int,
    data: RubricUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    r = RubricService.update(session, rubric_id, data)
    if not r:
        raise HTTPException(404, "Rubric not found")
     
    return success_response(data=r, message="Rubric updated")


# Admin: delete rubric
@router.delete("/{rubric_id}")
def delete_rubric(
    rubric_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    success = RubricService.delete(session, rubric_id)
    if not success:
        raise HTTPException(404, "Rubric not found")
 
    return success_response(message="Rubric deleted")
