from sqlmodel import Session, select
from models.rubric import Rubric
from schemas.rubric import RubricCreate, RubricUpdate


class RubricService:

    @staticmethod
    def get_by_question(session: Session, question_id: int):
        stmt = select(Rubric).where(Rubric.question_id == question_id)
        return session.exec(stmt).all()

    @staticmethod
    def get_by_id(session: Session, rubric_id: int):
        return session.get(Rubric, rubric_id)


    @staticmethod
    def create(session: Session, question_id: int, data: RubricCreate):
        r = Rubric(
            question_id=question_id,
            score=data.score,
            description=data.description
        )
        session.add(r)
        session.commit()
        session.refresh(r)
        return r

    @staticmethod
    def update(session: Session, rubric_id: int, data: RubricUpdate):
        r = session.get(Rubric, rubric_id)
        if not r:
            return None

        if data.score is not None:
            r.score = data.score
        if data.description is not None:
            r.description = data.description

        session.add(r)
        session.commit()
        session.refresh(r)
        return r

    @staticmethod
    def delete(session: Session, rubric_id: int):
        r = session.get(Rubric, rubric_id)
        if not r:
            return False

        session.delete(r)
        session.commit()
        return True
