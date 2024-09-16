from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base


class Questions(Base):
    __tablename__ = "questions"

    tran_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)


class Choices(Base):
    __tablename__ = "choices"

    tran_id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.tran_id"))
