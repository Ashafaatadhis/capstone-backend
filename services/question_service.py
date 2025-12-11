from sqlmodel import Session, select
from models.question import Question
from schemas.question import QuestionCreate, QuestionUpdate


class QuestionService:

    @staticmethod
    def get_all(session: Session,):
        stmt = select(Question)
        return session.exec(stmt).all()

    @staticmethod
    def get_by_id(session: Session, question_id: int):
        return session.get(Question, question_id)

    @staticmethod
    def create(session: Session, data: QuestionCreate):
        q = Question(text=data.text)
        session.add(q)
        session.commit()
        session.refresh(q)
        return q

    @staticmethod
    def update(session: Session, question_id: int, data: QuestionUpdate):
        q = session.get(Question, question_id)
        if not q:
            return None

        if data.text is not None:
            q.text = data.text

        session.add(q)
        session.commit()
        session.refresh(q)
        return q

    @staticmethod
    def delete(session: Session, question_id: int):
        q = session.get(Question, question_id)
        if not q:
            return False

        session.delete(q)
        session.commit()
        return True
