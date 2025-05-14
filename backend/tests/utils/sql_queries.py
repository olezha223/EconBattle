# SQL-скрипт для инициализации
INIT_COMMANDS = [
    """
    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        username TEXT NOT NULL,
        student_rating INTEGER NOT NULL DEFAULT 1000,
        teacher_rating INTEGER NOT NULL DEFAULT 1000
    );
    """,
    """
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        creator_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        text TEXT NOT NULL,
        price INTEGER,
        task_type VARCHAR NOT NULL,
        value JSONB NOT NULL,
        correct_value JSONB NOT NULL,
        access_type VARCHAR NOT NULL DEFAULT 'public'
    );
    """,
    """
    CREATE TABLE competitions (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR NOT NULL,
        creator_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        -- competition settings
        max_players INTEGER NOT NULL,
        max_rounds INTEGER NOT NULL,
        round_time_in_seconds INTEGER NOT NULL,
        tasks_markup JSONB NOT NULL
    );
    """,
    """
    CREATE TABLE rounds (
        id SERIAL PRIMARY KEY,
        player_1 TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        player_2 TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        points_player_1 INTEGER NOT NULL,
        points_player_2 INTEGER NOT NULL,
        status_player_1 VARCHAR NOT NULL,
        status_player_2 VARCHAR NOT NULL
    );
    """,
    """
    CREATE TABLE games (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        competition_id INTEGER NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
        player_1 TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        player_2 TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        rounds INTEGER[] NOT NULL DEFAULT ARRAY[]::INTEGER[],
        status_player_1 VARCHAR NOT NULL,
        status_player_2 VARCHAR NOT NULL,
        rating_difference_player_1 INTEGER NOT NULL,
        rating_difference_player_2 INTEGER NOT NULL,
        score_player_1 INTEGER NOT NULL,
        score_player_2 INTEGER NOT NULL
    );
    """,
]

# Скрипт для очистки таблиц
def get_cleanup_script(table: str):
    return f"DROP TABLE {table} CASCADE;"

CLEANUP_SCRIPTS = [
    get_cleanup_script(table) for table in ['tasks', 'games', 'rounds', 'competitions', 'users']
]

