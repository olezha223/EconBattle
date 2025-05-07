from tests.conftest import user_1_dto, user_2_dto, create_users, user_repo

async def test_create_one(user_repo):
    admin_id = await user_repo.create_with_username("admin", user_id='1')
    assert admin_id == '1'

async def test_create_similar_2(user_repo):
    admin_id_1 = await user_repo.create_with_username("admin", user_id='1')
    admin_id_2 = await user_repo.create_with_username("admin", user_id='1')
    assert admin_id_1 == '1'
    assert admin_id_2 == '1'

async def test_create_two(user_repo):
    admin_id = await user_repo.create_with_username("admin", user_id='1')
    other_id = await user_repo.create_with_username("other", user_id='2')
    assert admin_id == '1'
    assert other_id == '2'

async def test_get(user_1_dto, user_repo):
    admin_id = await user_repo.create_with_username("user_1", user_id='1')
    admin = await user_repo.get_by_username("user_1")
    assert admin_id == '1'
    assert admin == user_1_dto

async def test_get_two(user_1_dto, user_2_dto, user_repo):
    admin_id = await user_repo.create_with_username("user_1", user_id='1')
    other_id = await user_repo.create_with_username("user_2", user_id='2')
    assert admin_id == '1'
    assert other_id == '2'

    admin = await user_repo.get_by_username("user_1")
    other = await user_repo.get_by_username("user_2")
    assert admin == user_1_dto
    assert other == user_2_dto


async def test_get_not_existing(user_repo):
    user = await user_repo.get_by_username("foo")
    assert user is None


async def test_update_rating(create_users, user_repo):
    await user_repo.update_teacher_rating(rating_difference=-1000, user_id='1')
    user_1 = await user_repo.get_by_username("user_1")
    assert user_1.teacher_rating == 0

    await user_repo.update_student_rating(rating_difference=10000, user_id='1')
    user_1 = await user_repo.get_by_username("user_1")
    assert user_1.student_rating == 11000

    await user_repo.update_student_rating(rating_difference=1000, user_id='2')
    user_2 = await user_repo.get_by_username("user_2")
    assert user_2.student_rating == 2000

    await user_repo.update_teacher_rating(rating_difference=-1000, user_id='2')
    user_2 = await user_repo.get_by_username("user_2")
    assert user_2.teacher_rating == 0