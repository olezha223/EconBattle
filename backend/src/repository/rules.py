from sqlalchemy import select, func, insert

from src.database.schemas import Rule
from src.models.rules import RulesDTO
from src.repository import RepoInterface


class RulesRepo(RepoInterface):
    ...