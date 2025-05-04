# SQL-скрипт для инициализации
INIT_COMMANDS = [
    "CREATE TYPE task_type AS ENUM ('multiple choice', 'single choice', 'one word answer', 'one number answer');",
    "CREATE TYPE answer_type AS ENUM ('string', 'float', 'int', 'list_int', 'list_float');",
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
        type task_type NOT NULL,
        FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE answers (
        id SERIAL PRIMARY KEY,
        task_id INTEGER NOT NULL,
        type answer_type NOT NULL,
        value JSONB NOT NULL,
        correct_value JSONB NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
    );
    """
]

# Скрипт для очистки таблиц
def get_cleanup_script(table: str):
    return f"DROP TABLE {table} CASCADE;"

CLEANUP_SCRIPTS = [
    get_cleanup_script(table) for table in ['answers', 'tasks', 'users']
] + ['DROP TYPE IF EXISTS task_type, answer_type;']

