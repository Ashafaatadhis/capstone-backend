from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOWED_ORIGINS
from database import init_db, engine
from routers import auth, question, rubric, grading
from utils.seed_admin import seed_admin
from sqlmodel import Session

from models.user import User
from models.question import Question
from models.rubric import Rubric

 

app = FastAPI(
    title="AI Interview Backend",
    version="1.0.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Run this when app starts
@app.on_event("startup")
def on_startup():
    init_db()

    # Seed admin correctly
    from sqlmodel import Session
    from utils.seed_admin import seed_admin

    with Session(engine) as session:
        seed_admin(session)




# Register routers (AUTH already exists)
app.include_router(auth.router)

# Question + Rubric routers will be added later in step CRUD
# app.include_router(question.router)
# app.include_router(rubric.router)


app.include_router(auth.router)
app.include_router(question.router)
app.include_router(rubric.router)
app.include_router(grading.router)


@app.get("/")
def root():
    return {"message": "AI Interview Backend is running"}
