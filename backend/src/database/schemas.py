from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.models.problems import TaskTypeEnum, AnswerTypeEnum

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'users'

    username = Column(String(255), unique=True, nullable=False)
    student_rating = Column(Integer, default=1000, nullable=False)
    teacher_rating = Column(Integer, default=1000, nullable=False)




class Problem(Base):
    __tablename__ = "tasks"

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    price = Column(Integer, nullable=True)
    task_type = Column(String, nullable=False)
    answer_type = Column(String, nullable=False)
    value = Column(JSON, nullable=False)
    correct_value = Column(JSON, nullable=False)


class Match(Base):
    __tablename__ = 'matches'

    player1_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    player2_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    winner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())
    total_rounds = Column(Integer, nullable=False)


class Round(Base):
    __tablename__ = 'rounds'

    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    round_number = Column(Integer, nullable=False)
    player1_score = Column(Integer, default=0)
    player2_score = Column(Integer, default=0)
    problems = Column(JSON, nullable=False)  # Список ID задач [1, 5, 3]
