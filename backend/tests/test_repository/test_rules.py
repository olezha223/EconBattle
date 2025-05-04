from src.models.rules import RulesDTO
from src.repository.rules import RulesRepo
from tests.utils.adapter import get_session_test

rules_repo = RulesRepo(session_getter=get_session_test)

async def test_create():
    rule = RulesDTO(
        max_players=1,
        max_rounds = 1,
        round_time_in_seconds = 1,
        tasks_markup = {"round_1": [1, 2, 3]}
    )

    rule_id = await rules_repo.create(rule)

    assert rule_id == 1


async def test_create_multiple():
    rule = RulesDTO(
        max_players=1,
        max_rounds=1,
        round_time_in_seconds=1,
        tasks_markup={"round_1": [1, 2, 3]}
    )

    rule_id = await rules_repo.create(rule)

    assert rule_id == 1

    rule = RulesDTO(
        max_players=1,
        max_rounds=1,
        round_time_in_seconds=10,
        tasks_markup={"round_1": [3, 2, 1]}
    )

    rule_id = await rules_repo.create(rule)

    assert rule_id == 2


async def test_get():
    test_rule_1 = RulesDTO(
        max_players=1,
        max_rounds=1,
        round_time_in_seconds=1,
        tasks_markup={"round_1": [1, 2, 3]}
    )

    rule_id_1 = await rules_repo.create(test_rule_1)

    assert rule_id_1 == 1

    test_rule_2 = RulesDTO(
        max_players=1,
        max_rounds=1,
        round_time_in_seconds=10,
        tasks_markup={"round_1": [3, 2, 1]}
    )

    rule_id_2 = await rules_repo.create(test_rule_2)

    assert rule_id_2 == 2

    rule_1 = await rules_repo.get(rule_id_1)
    assert rule_1 == test_rule_1

    rule_2 = await rules_repo.get(rule_id_2)
    assert rule_2 == test_rule_2