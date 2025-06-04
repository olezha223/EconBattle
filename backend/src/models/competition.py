from datetime import datetime

from pydantic import BaseModel, Field


class Round(BaseModel):
    """Схема раунда игры"""
    tasks: list[int] = Field(..., max_length=50)
    time_limit: int = Field(60, gt=0, lt=3000)

class NewCompetition(BaseModel):
    """Схема создаваемого игроком соревнования"""
    name: str = Field(..., min_length=1, max_length=50)
    creator_id: str = Field(...)
    # settings
    max_rounds: int = Field(..., gt=0, le=30)
    tasks_markup: dict[str, Round] = Field(..., examples=[
        {
            "1": {
                "tasks": [
                    18,
                    19,
                    20
                ],
                "time_limit": 60
            }
        },
    ])

class CompetitionDTO(NewCompetition):
    """Исходная схема соревнования + поля из базы данных"""
    id: int
    created_at: datetime

class CompetitionDetailedDTO(CompetitionDTO):
    """Соревнование с бизнес-метриками"""
    creator_name: str
    picture: str
    max_time: int = Field(..., gt=0, title="Максимальное время, которон может занять соревнование")
    mean_task_difficulty: float = Field(..., gt=0, le=1000, title="Средняя сложность задач в соревновании")
    percent_of_correct: float = Field(..., ge=0, le=100, title="Процент решенных правильно задач в статистике игр")

class CompetitionPreview(BaseModel):
    """Превью соревнования в разные ленты, в основном бизнес-метриками"""
    id: int
    name: str
    games_played: int = Field(..., ge=0, title="Число сыгранных игр в этом соревновании")
    unique_players: int = Field(..., ge=0, title="Сколько уникальных игроков играло в это соревнование")
    created_at: datetime
    creator_id: str
    creator_name: str
    picture: str
    mean_task_difficulty: float = Field(..., gt=0, le=1000, title="Средняя сложность задач в соревновании")
