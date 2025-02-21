from typing import Any

from pydantic import BaseModel


class ProblemDTO(BaseModel):
    id: int
    question_text: str
    answers: dict[str, Any]
    price: int
