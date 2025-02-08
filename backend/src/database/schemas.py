from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    rating = Column(Integer, default=1000)


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False)
    answers = Column(JSON, nullable=False)
    price = Column(Integer, default=100)


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    player2_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    winner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())
    total_rounds = Column(Integer, nullable=False)


class Round(Base):
    __tablename__ = 'rounds'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    round_number = Column(Integer, nullable=False)
    player1_score = Column(Integer, default=0)
    player2_score = Column(Integer, default=0)
    problems = Column(JSON, nullable=False)  # Список ID задач [1, 5, 3]
