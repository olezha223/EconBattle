from sqlalchemy import select, func, insert

from src.database.schemas import Task
from src.models.problems import TaskDTO
from src.repository import RepoInterface


class TaskRepo(RepoInterface):
    ...