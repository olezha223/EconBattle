-- Создание таблицы users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    rating INT DEFAULT 1000
);

-- Создание таблицы problems
CREATE TABLE problems (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    answers JSON NOT NULL,
    price INT DEFAULT 100
);

-- Создание таблицы matches
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    player1_id INT NOT NULL REFERENCES users(id),
    player2_id INT NOT NULL REFERENCES users(id),
    winner_id INT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_rounds INT NOT NULL
);

-- Создание таблицы rounds
CREATE TABLE rounds (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(id),
    round_number INT NOT NULL,
    player1_score INT DEFAULT 0,
    player2_score INT DEFAULT 0,
    problems JSON NOT NULL
);

-- Добавление тестовых данных в таблицу users
INSERT INTO users (username, rating) VALUES
('Misha', 1100),
('Oleg', 1000),
('charlie', 1050);

-- Добавление тестовых данных в таблицу problems
INSERT INTO problems (question_text, answers, price) VALUES
('What is 2 + 2?', '{"options": ["3", "4", "5"], "correct": "4"}', 100),
('What is the capital of France?', '{"options": ["Berlin", "Madrid", "Paris"], "correct": "Paris"}', 150),
('What is the square root of 16?', '{"options": ["2", "4", "8"], "correct": "4"}', 200);

-- Добавление тестовых данных в таблицу matches
INSERT INTO matches (player1_id, player2_id, winner_id, total_rounds) VALUES
(1, 2, 1, 3),  -- Матч между alice и bob, победитель alice
(2, 3, 3, 5);  -- Матч между bob и charlie, победитель charlie

-- Добавление тестовых данных в таблицу rounds
INSERT INTO rounds (match_id, round_number, player1_score, player2_score, problems) VALUES
(1, 1, 10, 5, '[1, 2]'),  -- Раунд 1 матча 1, задачи с id 1 и 2
(1, 2, 15, 10, '[3]'),     -- Раунд 2 матча 1, задача с id 3
(2, 1, 5, 10, '[1, 3]');   -- Раунд 1 матча 2, задачи с id 1 и 3