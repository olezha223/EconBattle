from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TaskTypeEnum(str, Enum):
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE'
    SINGLE_CHOICE = 'SINGLE_CHOICE'
    ONE_WORD_ANSWER = 'ONE_WORD_ANSWER'
    ONE_NUMBER_ANSWER = 'ONE_NUMBER_ANSWER'


class AnswerTypeEnum(str, Enum):
    STRING = "STRING"
    FLOAT = "FLOAT"
    INT = "INT"
    LIST_INT = "LIST_INT"
    LIST_FLOAT = "LIST_FLOAT"


class TaskFromAuthor(BaseModel):
    """Схема от автора задачи"""
    creator_id: str = Field(...)
    name: str = Field(..., min_length=1, max_length=50, title="Название задачи")
    text: str = Field(..., min_length=1, max_length=2000, title="Условие задачи")
    price: int = Field(..., gt=0, le=1000, title="Сложность задачи")
    task_type: str = Field(..., title='Тип задачи (одиночный, множ. выбор и так далее)')
    value: dict[str, Any] = Field(
        ...,
        examples=[
            {
                "answers": [
                    "[0 %; 5 %)", "[5 %; 10 %)",
                    "[10 %; 15 %)", "[15 %; 20 %]"
                ]
            },
            {
                "answers": [1, 2, 3]
            }
        ],
        title="Все возможные ответы на задачу"
    )
    correct_value: dict[str, Any] = Field(..., title="Правильный ответ(ы) в зависимости от типа задачи", examples=[
        {
            "answers": [
                "[0 %; 5 %)"
            ]
        },
        {
            "answers": [
                80
            ]
        }
    ])
    access_type: str = Field(..., title="Модификатор доступа (публичный или приватный)")


class TaskWithoutAnswers(BaseModel):
    """Задача из базы данных, но без ответов, используется для отправки пользователю в игре"""
    id: int
    creator_id: str
    created_at: datetime
    name: str
    text: str
    price: int
    task_type: str
    value: dict[str, Any]

class TaskDTO(TaskWithoutAnswers):
    """Задача из базы данных с ответами и модификатором доступа, используется для проверки ответов и доступа"""
    correct_value: dict[str, Any]
    access_type: str

class TaskDetailedDTO(TaskDTO):
    """Задача вместе с именем автора и его аватаркой"""
    creator_name: str
    picture: str

class TaskPreview(BaseModel):
    """Превью задачи во все возможные ленты"""
    id: int
    # блок инфы про автора
    created_at: datetime
    creator_id: str
    # блок инфы про задачу
    name: str
    used_in_competitions: int = Field(..., ge=0, title="Сколько раз задачу использовали в соревнованиях")
    creator_name: str
    picture: str
    price: int
    access_type: str
    correct_percent: float = Field(..., ge=0, le=100, title="Процент правильных попыток решения задачи")

class TaskForGame(BaseModel):
    """Еще одна схема для задачи для игрока (без ответов), но со строковой датой"""
    id: int
    creator_id: str
    created_at: str
    name: str
    text: str
    price: int
    task_type: str
    value: dict[str, Any]