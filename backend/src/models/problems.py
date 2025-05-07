from enum import Enum
from typing import Any

from pydantic import BaseModel

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
    creator_id: str
    name: str
    text: str
    price: int
    task_type: str
    value: dict[str, Any]
    answer_type: str
    correct_value: dict[str, Any]


class TaskWithoutAnswers(BaseModel):
    id: int
    creator_id: str
    name: str
    text: str
    price: int
    task_type: str
    value: dict[str, Any]
    answer_type: str

class TaskDTO(TaskWithoutAnswers):
    correct_value: dict[str, Any]