from tests.conftest import redis_queue

async def test_insert(redis_queue):
    competition_id = 1
    player_id = '100'
    redis_queue.insert_player(competition_id, player_id)
    assert redis_queue.check_exists(competition_id, player_id)

async def test_remove_player(redis_queue):
    competition_id = 1
    player_id = '100'
    redis_queue.insert_player(competition_id, player_id)
    redis_queue.remove_player(competition_id, player_id)
    assert not redis_queue.check_exists(competition_id, player_id)

async def test_check_exists(redis_queue):
    competition_id = 1
    player_id = '100'
    assert not redis_queue.check_exists(competition_id, player_id)
    redis_queue.insert_player(competition_id, player_id)
    assert redis_queue.check_exists(competition_id, player_id)

async def test_get_len(redis_queue):
    competition_id = 1
    assert redis_queue.get_len(competition_id) == 0
    redis_queue.insert_player(competition_id, '100')
    redis_queue.insert_player(competition_id, '101')
    assert redis_queue.get_len(competition_id) == 2

async def test_first(redis_queue):
    competition_id = 1
    assert redis_queue.first(competition_id) is None
    redis_queue.insert_player(competition_id, '100')
    redis_queue.insert_player(competition_id, '101')
    assert redis_queue.first(competition_id) == '100'

async def test_get_first_2(redis_queue):
    competition_id = 1
    assert redis_queue.get_first_2(competition_id) == []
    redis_queue.insert_player(competition_id, '100')
    assert redis_queue.get_first_2(competition_id) == ['100']
    redis_queue.insert_player(competition_id, '101')
    assert redis_queue.get_first_2(competition_id) == ['100', '101']
    redis_queue.insert_player(competition_id, '102')
    assert redis_queue.get_first_2(competition_id) == ['100', '101']

async def test_pop(redis_queue):
    competition_id = 1
    assert redis_queue.pop(competition_id) is None
    redis_queue.insert_player(competition_id, '100')
    redis_queue.insert_player(competition_id, '101')
    assert redis_queue.pop(competition_id) == '100'
    assert redis_queue.pop(competition_id) == '101'
    assert redis_queue.pop(competition_id) is None

async def test_get_all(redis_queue):
    competition_id = 1
    assert redis_queue.get_all(competition_id) == []
    redis_queue.insert_player(competition_id, '100')
    redis_queue.insert_player(competition_id, '101')
    redis_queue.insert_player(competition_id, '102')
    assert redis_queue.get_all(competition_id) == ['100', '101', '102']