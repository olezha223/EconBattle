from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, func, Text
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(Text, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    username = Column(Text, nullable=False)
    student_rating = Column(Integer, default=1000, nullable=False)
    teacher_rating = Column(Integer, default=1000, nullable=False)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    creator_id = Column(Text, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    task_type = Column(String, nullable=False)
    answer_type = Column(String, nullable=False)
    value = Column(JSON, nullable=False)
    correct_value = Column(JSON, nullable=False)


class Competition(Base):
    __tablename__ = 'competitions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    name = Column(String, nullable=False)
    creator_id = Column(Text, ForeignKey('users.id'), nullable=False)

    # настройки игры
    max_players = Column(Integer, nullable=False)
    max_rounds = Column(Integer, nullable=False)
    round_time_in_seconds = Column(Integer, nullable=False)
    tasks_markup = Column(JSON, nullable=False)


class Round(Base):
    __tablename__ = "rounds"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    points_player_1 = Column(Integer, nullable=False)
    points_player_2 = Column(Integer, nullable=False)
    status_player_1 = Column(String, nullable=False)
    status_player_2 = Column(String, nullable=False)


class Game(Base):
    __tablename__ = 'games'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)

    player_1 = Column(Text, ForeignKey('users.id'), nullable=False)
    player_2 = Column(Text, ForeignKey('users.id'), nullable=False)
    rounds = Column(ARRAY(Integer), default=[], nullable=False)
    status_player_1 = Column(String, nullable=False)
    status_player_2 = Column(String, nullable=False)
    rating_difference_player_1 = Column(Integer, nullable=False)
    rating_difference_player_2 = Column(Integer, nullable=False)
    score_player_1 = Column(Integer, nullable=False)
    score_player_2 = Column(Integer, nullable=False)