from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, func
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = 'users'

    username = Column(String(255), unique=True, nullable=False)
    student_rating = Column(Integer, default=1000, nullable=False)
    teacher_rating = Column(Integer, default=1000, nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    task_type = Column(String, nullable=False)
    answer_type = Column(String, nullable=False)
    value = Column(JSON, nullable=False)
    correct_value = Column(JSON, nullable=False)


class Rule(Base):
    __tablename__ = "rules"
    max_players = Column(Integer, nullable=False)
    max_rounds = Column(Integer, nullable=False)
    round_time_in_seconds = Column(Integer, nullable=False)
    tasks_markup = Column(JSON, nullable=False)


class Round(Base):
    __tablename__ = "rounds"
    points_player_1 = Column(Integer, nullable=False)
    points_player_2 = Column(Integer, nullable=False)
    status_player_1 = Column(String, nullable=False)
    status_player_2 = Column(String, nullable=False)


class Game(Base):
    __tablename__ = 'games'

    player_1 = Column(Integer, ForeignKey('users.id'), nullable=False)
    player_2 = Column(Integer, ForeignKey('users.id'), nullable=False)
    rounds = Column(ARRAY(Integer), default=[], nullable=False)
    status_player_1 = Column(String, nullable=False)
    status_player_2 = Column(String, nullable=False)
    rating_difference_player_1 = Column(Integer, nullable=False)
    rating_difference_player_2 = Column(Integer, nullable=False)

class Competition(Base):
    __tablename__ = 'competitions'

    played_games = Column(ARRAY(Integer), default=[], nullable=False)
    name = Column(String, nullable=False)
    rules = Column(Integer, ForeignKey('rules.id'), nullable=False)
    tasks = Column(ARRAY(Integer), default=[], nullable=False)
    creator = Column(Integer, ForeignKey('users.id'), nullable=False)