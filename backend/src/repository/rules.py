from sqlalchemy import select, func, insert

from src.database.schemas import Rule
from src.models.rules import RulesDTO
from src.repository import RepoInterface


class RulesRepo(RepoInterface):
    async def create(self, rule: RulesDTO) -> int:
        async with self.session_getter() as session:
            result = await session.execute(
                insert(Rule).values(**rule.model_dump())
                .returning(Rule.id)
            )
            rule_id = result.scalar()
            return rule_id

    async def get(self, rule_id: int) -> RulesDTO:
        async with self.session_getter() as session:
            result = await session.execute(
                select(Rule)
                .where(Rule.id == rule_id)
            )
            rule = result.scalar()
            return RulesDTO.model_validate(rule, from_attributes=True)