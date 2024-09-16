from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, Session_local

app = FastAPI()

# Will create all the tables in db that are defined in models file
models.Base.metadata.create_all(bind=engine)


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_db():
    db = Session_local()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session_local, Depends(get_db)]


# get the particular question_id's data
@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = (
        db.query(models.Questions)
        .filter(models.Questions.tran_id == question_id)
        .first()
    )
    print("\n result of the following question : " + str(result))

    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")

    return result


@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = (
        db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    )
    print("\n result of the following question : " + str(result))

    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")

    return result


@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.tran_id,
        )
        db.add(db_choice)

    db.commit()
    db.refresh(db_choice)
