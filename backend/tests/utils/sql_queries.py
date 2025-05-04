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
        creator_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        text TEXT NOT NULL,
        price INTEGER,
        task_type VARCHAR NOT NULL,
        value JSONB NOT NULL,
        answer_type VARCHAR NOT NULL,
        correct_value JSONB NOT NULL,
        FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
]

# Скрипт для очистки таблиц
def get_cleanup_script(table: str):
    return f"DROP TABLE {table} CASCADE;"

CLEANUP_SCRIPTS = [
    get_cleanup_script(table) for table in ['tasks', 'users']
]

