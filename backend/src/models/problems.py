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
    creator_id: str = Field(...)
    name: str = Field(..., min_length=1, max_length=50)
    text: str = Field(..., min_length=1, max_length=2000)
    price: int = Field(..., gt=0, le=1000)
    task_type: str = Field(..., examples=[
        TaskTypeEnum.MULTIPLE_CHOICE.value,
        TaskTypeEnum.SINGLE_CHOICE.value,
        TaskTypeEnum.ONE_WORD_ANSWER.value,
        TaskTypeEnum.ONE_NUMBER_ANSWER.value
    ])
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
        ]
    )
    correct_value: dict[str, Any] = Field(..., examples=[
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
    access_type: str = Field(..., examples=[
        AnswerTypeEnum.STRING.value,
        AnswerTypeEnum.FLOAT.value,
        AnswerTypeEnum.LIST_INT.value,
        AnswerTypeEnum.LIST_FLOAT.value
    ])


class TaskWithoutAnswers(BaseModel):
    id: int
    creator_id: str
    created_at: datetime
    name: str
    text: str
    price: int
    task_type: str
    value: dict[str, Any]

class TaskDTO(TaskWithoutAnswers):
    correct_value: dict[str, Any]
    access_type: str

class TaskDetailedDTO(TaskDTO):
    creator_name: str
    picture: str

class TaskPreview(BaseModel):
    id: int
    # блок инфы про автора
    created_at: datetime
    creator_id: str
    # блок инфы про задачу
    name: str
    used_in_competitions: int
    creator_name: str
    picture: str
    price: int
    access_type: str
    correct_percent: float

class TaskForGame(BaseModel):
    id: int
    creator_id: str
    created_at: str
    name: str
    text: str
    price: int
    task_type: str
    value: dict[str, Any]