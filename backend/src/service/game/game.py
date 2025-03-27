import asyncio

from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from src.models.game import EventType
from src.models.problems import ProblemDTO
from src.models.users import UserDTO, Player
from src.repository.problems import ProblemsRepo


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.problems_repo = ProblemsRepo()
        self.players: dict[int, UserDTO] = {
            player1.user.id: player1.user,
            player2.user.id: player2.user
        }
        self.sockets: dict[int, WebSocket] = {
            player1.user.id: player1.websocket,
            player2.user.id: player2.websocket
        }
        self.locks: dict[int, asyncio.Lock] = {
            player1.user.id: asyncio.Lock(),
            player2.user.id: asyncio.Lock()
        }

        self.rounds = []
        self.current_round = 0
        self.scores = {player1.user.id: 0, player2.user.id: 0}
        self.wins = {player1.user.id: 0, player2.user.id: 0}

    async def start(self):
        try:
            await self._notify_players("Game", data={"msg": "Идет процесс игры"})
            while self.current_round < 2:
                print(f"Начинаем раунд {self.current_round}")
                await self._start_round()
                self.current_round += 1
        except asyncio.CancelledError:
            # Обработка прерывания игры
            print("Игра прервана")
        finally:
            print(f"Позвали клинап для игры между {self.players}")
            await self._cleanup()

    async def _cleanup(self):
        for player in self.players.values():
            ws = self.sockets.get(player.id)
            if ws and ws.client_state == WebSocketState.CONNECTED:
                try:
                    await ws.send_json({"type": "Closing", "msg": f"{player.id} closing"})
                    await ws.close()
                except Exception as e:
                    print(str(e))

    async def _notify_players(self, event_type: str, data: dict = None):
        message = {"type": event_type}
        if data:
            message.update(data)

        for player in self.players.values():
            ws = self.sockets.get(player.id)
            if (not ws) or (ws.client_state != WebSocketState.CONNECTED):
                continue

            await ws.send_json(message)

    async def _start_round(self):
        problems = await self.problems_repo.get_random_problems(3)
        await self._notify_players(
            event_type="Start Round",
            data={
                "problems": [p.model_dump() for p in problems],
                "time_limit": 120
            }
        )

        # Бэкенд ждет на 10 секунд дольше
        answers = await self._collect_answers(timeout=130)

        print(answers)
        scores = self._calculate_scores(answers, problems)
        print(scores)
        # await self._update_scores(scores)

    async def _collect_answers(self, timeout: int):
        tasks = {
            asyncio.create_task(self._wait_for_answer(player_id, self.locks[player_id]))
            for player_id in self.players
        }

        try:
            # Ждем ВСЕ ответы в течение timeout секунд
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            print("Время на ответы вышло")
            pass

        # Собираем результаты
        answers = {}
        for task in tasks:
            if task.done() and not task.cancelled():
                try:
                    player_id, result = task.result()
                    answers[player_id] = result
                except Exception as e:
                    print("Неожиданная ошибкак при сборе результатов", str(e))

        # Отменяем оставшиеся задачи
        for task in tasks:
            if not task.done():
                task.cancel()

        return answers

    async def _wait_for_answer(self, player_id: int, lock: asyncio.Lock) -> tuple[int, list[int]]:
        """Ожидание ответа от конкретного игрока с блокировкой"""
        async with lock:
            try:
                if self.sockets[player_id].client_state == WebSocketState.CONNECTED:
                    data = await self.sockets[player_id].receive_json()
                    print(data, player_id)
                    return player_id, data.get("answers", [])
                return player_id, []
            except (WebSocketDisconnect, RuntimeError):
                return player_id, []

    def _calculate_scores(self, answers: dict, problems: list[ProblemDTO]) -> dict:
        """Расчет очков за раунд"""
        scores = {pid: 0 for pid in self.players}
        for pid, user_answer in answers.items():
            for problem in problems:
                problem_id = problem.id
                user_answer = user_answer[problem_id]
                if user_answer == problem.answers['correct']:
                    scores[pid] += problem["price"]
        return scores

    # async def _update_scores(self, scores: dict):
    #     """Обновление счетчиков побед"""
    #     max_score = max(scores.values())
    #     for pid, score in scores.items():
    #         self.scores[pid] += score
    #         if score == max_score and score > 0:
    #             self.wins[pid] += 1
    #
    #     # Отправка результатов раунда
    #     results = {
    #         "type": EventType.ROUND_RESULT.value,
    #         "scores": scores,
    #         "total_wins": self.wins
    #     }
    #     for ws in self.sockets.values():
    #         await ws.send_json(results)

    # async def _end_game(self):
    #     """Финализация игры и обновление рейтингов"""
    #     winner_id = max(self.wins, key=self.wins.get)
    #     if self.wins[winner_id] < 2:
    #         winner_id = None  # Ничья, если никто не набрал 2 победы
    #
    #     # Сохранение матча в БД
    #     async with get_session() as session:
    #         match = Match(
    #             player1_id=self.players[list(self.players)[0]].id,
    #             player2_id=self.players[list(self.players)[1]].id,
    #             winner_id=winner_id
    #         )
    #         session.add(match)
    #         await session.commit()
    #
    #         # Сохранение раундов
    #         for round_num in range(self.current_round):
    #             await session.execute(
    #                 insert(Round).values(
    #                     match_id=match.id,
    #                     round_number=round_num,
    #                     problems=json.dumps(
    #                         [p["id"] for p in self.rounds[round_num]["problems"]]
    #                     ),
    #                     player1_score=self.rounds[round_num]["scores"][list(self.players)[0]],
    #                     player2_score=self.rounds[round_num]["scores"][list(self.players)[1]]
    #                 )
    #             )
    #         await session.commit()
    #
    #     # Обновление рейтинга
    #     if winner_id:
    #         await self._update_rating(winner_id)
    #
    #     # Отправка финальных результатов
    #     final_message = {
    #         "type": EventType.GAME_END.value,
    #         "winner_id": winner_id,
    #         "final_scores": self.scores
    #     }
    #     for ws in self.sockets.values():
    #         await ws.send_json(final_message)
    #
    # async def _update_rating(self, winner_id: int):
    #     """Обновление рейтинга в БД"""
    #     async with get_session() as session:
    #         for pid in self.players:
    #             user = await session.get(User, pid)
    #             user.rating += 10 if pid == winner_id else -10
    #         await session.commit()
