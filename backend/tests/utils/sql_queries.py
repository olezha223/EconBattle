# SQL-скрипт для инициализации
INIT_COMMANDS = [
    """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        student_rating INTEGER NOT NULL DEFAULT 1000,
        teacher_rating INTEGER NOT NULL DEFAULT 1000,
        played_games INTEGER NOT NULL DEFAULT 0,
        created_competitions INTEGER NOT NULL DEFAULT 0
    );
    """,
    """
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        creator_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        text TEXT NOT NULL,
        price INTEGER,
        task_type VARCHAR NOT NULL,
        value JSONB NOT NULL,
        answer_type VARCHAR NOT NULL,
        correct_value JSONB NOT NULL
    );
    """,
    """
    CREATE TABLE rules (
        id SERIAL PRIMARY KEY,
        max_players INTEGER NOT NULL,
        max_rounds INTEGER NOT NULL,
        round_time_in_seconds INTEGER NOT NULL,
        tasks_markup JSONB NOT NULL
    );
    """,
    """
    CREATE TABLE games (
        id SERIAL PRIMARY KEY,
        player_1 INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        player_2 INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        rounds INTEGER[] NOT NULL DEFAULT ARRAY[]::INTEGER[],
        status_player_1 VARCHAR NOT NULL,
        status_player_2 VARCHAR NOT NULL,
        rating_difference_player_1 INTEGER NOT NULL,
        rating_difference_player_2 INTEGER NOT NULL
    );
    """
]

# Скрипт для очистки таблиц
def get_cleanup_script(table: str):
    return f"DROP TABLE {table} CASCADE;"

CLEANUP_SCRIPTS = [
    get_cleanup_script(table) for table in ['tasks', 'users', 'rules', 'games']
]

