from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import WebSocket


class UserDTO(BaseModel):
    """Базовая схема юзера при создании записи в базе данных"""
    id: str
    username: str
    picture: str
    student_rating: int = Field(default=1000, title="Рейтинг как студента, зависит от игр")
    teacher_rating: int = Field(default=1000, title="Рейтинг преподавателя, меняется от деятельности для платформы")

class UserData(UserDTO):
    """Базовая схема + время регистрации"""
    created_at: datetime

class UserInfo(UserData):
    """Расширенная схема для страницы пользователя"""
    user_activity: dict[datetime, int] = Field(
        ...,
        title="Активность пользователя на платформе: чем больше игр, "
              "решенных задач, созданных сущностей, тем выше значение"
    )
    # статистика как игрока
    wins_count: int
    losses_count: int
    tie_count: int
    games_played: int = Field(..., title="Сколько игр сыграл")

    # статистика как составителя задач и соревнований
    tasks_created: int = Field(..., title="Сколько создал задач на платформе")
    mean_task_difficulty: float = Field(..., title="Средняя сложность задач от этого автора")
    tasks_popularity_count: int = Field(..., title="Сколько было попыток решить его задачи")
    competitions_created: int = Field(..., title="Сколько создал соревнований на платформе")


class Player:
    """Это не класс! Это бесправный объект который просто удобно хранит данные!!! (с) Великий джавист"""
    def __init__(self, user: UserDTO, websocket: WebSocket):
        self.user: UserDTO = user
        self.websocket: WebSocket = websocket
