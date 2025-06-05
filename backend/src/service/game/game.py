import asyncio

from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect

from src.models.game import EventType, NewGame
from src.models.problems import TaskDTO, TaskWithoutAnswers
from src.models.round import StatusEnum, RoundDTO
from src.models.users import UserDTO, Player
from src.service import get_task_service, get_game_service, get_competition_service, get_user_service, \
    get_round_service, get_task_stats_service


class Game:
    def __init__(self, player1: Player, player2: Player, competition_id: int):
        self.task_service = get_task_service()
        self.game_service = get_game_service()
        self.competition_service = get_competition_service()
        self.user_service = get_user_service()
        self.round_service = get_round_service()
        self.tasks_stats_service = get_task_stats_service()

        self.user_1_id = player1.user.id
        self.user_2_id = player2.user.id

        self.players: dict[str, UserDTO] = {
            self.user_1_id: player1.user,
            self.user_2_id: player2.user,
        }
        self.sockets: dict[str, WebSocket] = {
            self.user_1_id: player1.websocket,
            self.user_2_id: player2.websocket
        }
        self.locks: dict[int, asyncio.Lock] = {
            self.user_1_id: asyncio.Lock(),
            self.user_2_id: asyncio.Lock()
        }

        self.player_final_info: dict[str, str] = {
            self.user_1_id: {"status": StatusEnum.TIE.value, "diff": 0},
            self.user_2_id: {"status": StatusEnum.TIE.value, "diff": 0},
        }

        self.competition_id = competition_id
        self.competition = None

        self.round_ids = []
        self.current_round = 0
        self.scores = {player1.user.id: 0, player2.user.id: 0}
        self.wins = {player1.user.id: 0, player2.user.id: 0}

    async def start(self):
        self.competition = await self.competition_service.get_competition(self.competition_id)
        try:
            await self._notify_players(
                "Game",
                data={
                    "msg": "Идет процесс игры",
                    "round_count": self.competition.max_rounds
                }
            )
            while self.current_round < self.competition.max_rounds: # итерируемся до последнего раунда
                print(f"Начинаем раунд {self.current_round}")
                await self._start_round()
                self.current_round += 1
            await self._end_game()
        except asyncio.CancelledError:
            # Обработка прерывания игры
            print("Игра прервана")
        finally:
            print(f"Позвали клинап для игры между {self.players}")
            await self._cleanup()

    async def _cleanup(self):
        """Очистка игры, закрытие всех соединений в конце игры или при остановке"""
        for player in self.players.values():
            # для каждого игрока закрываем его соединение и отправляем об этом информацию ему
            ws = self.sockets.get(player.id)
            if ws and ws.client_state == WebSocketState.CONNECTED:
                try:
                    await ws.send_json({"type": "Closing", "msg": f"{player.id} closing"})
                    await ws.close()
                except Exception as e:
                    print(str(e))

    async def _notify_players(self, event_type: str, data: dict = None):
        """Рассылка всем подключенным игрокам определенного сообщения"""
        message = {"type": event_type}
        if data:
            message.update(data)

        for player in self.players.values():
            ws = self.sockets.get(player.id)
            # безопасная отправка
            if (not ws) or (ws.client_state != WebSocketState.CONNECTED):
                continue

            await ws.send_json(message)

    async def _get_problems_for_round(self) -> list[TaskWithoutAnswers]:
        """Получаем задачи для раунда"""
        tasks = [
            await self.task_service.get(task_id) for task_id in
            self.competition.tasks_markup[str(self.current_round + 1)].tasks
        ]
        return tasks

    async def _start_round(self):
        """Инициализация раунда"""
        problems = await self._get_problems_for_round()
        time_limit = self.competition.tasks_markup[str(self.current_round + 1)].time_limit
        # отправляем задачи игрокам в начале раунда
        await self._notify_players(
            event_type="Start Round",
            data={
                "problems": [self.task_service.get_task_for_round(p).model_dump() for p in problems],
                "time_limit": time_limit - 10
            }
        )

        # Бэкенд ждет на 10 секунд дольше чтобы точно успели дойти ответы
        answers = await self._collect_answers(timeout=time_limit)

        print(answers)
        # Считаем очки игроков по полученным ответам
        scores = await self._calculate_scores(answers, problems)
        print(scores)
        # Обновляем внутренние переменные игры и отправляем результаты раунда игрокам
        await self._update_scores(scores)

    async def _collect_answers(self, timeout: int):
        """Сбор ответов на задачи"""
        # создаем группу задач с ожиданием ответов
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
            if task.done() and not task.cancelled(): # проверка, что мы еще не отменили задачу
                try:
                    player_id, result = task.result()
                    answers[player_id] = result
                except Exception as e:
                    print("Неожиданная ошибках при сборе результатов", str(e))

        # Отменяем оставшиеся задачи
        for task in tasks:
            if not task.done():
                task.cancel()

        return answers

    async def _wait_for_answer(self, player_id: int, lock: asyncio.Lock) -> tuple[int, list[int]]:
        """Ожидание ответа от конкретного игрока с блокировкой"""
        async with lock:
            try:
                if self.sockets[player_id].client_state == WebSocketState.CONNECTED: # защита от отключений
                    data = await self.sockets[player_id].receive_json() # ждем ответы
                    print(data, player_id)
                    return player_id, data.get("answers", {})
                return player_id, {}
            except (WebSocketDisconnect, RuntimeError):
                return player_id, {}

    async def _calculate_scores(self, answers: dict, problems: list[TaskDTO]) -> dict:
        """Расчет очков за раунд"""
        scores = {pid: 0 for pid in self.players}
        for pid, user_answer in answers.items():
            for problem in problems:
                problem_id = problem.id
                answer_list = user_answer.get(str(problem_id), None)
                # Добавляем в данные статистику по решенной задаче
                await self.tasks_stats_service.create(pid, problem, answer_list)
                if answer_list:
                    # Проверка решения
                    if answer_list == problem.correct_value.get("answers", []):
                        scores[pid] += problem.price
        return scores

    def _update_statues(self):
        score_1 = self.scores[self.user_1_id]
        score_2 = self.scores[self.user_2_id]

        if score_1 == score_2:
            # Ничья
            self.player_final_info[self.user_1_id] = {"status": StatusEnum.TIE.value, "diff": 0}
            self.player_final_info[self.user_2_id] = {"status": StatusEnum.TIE.value, "diff": 0}
        else:
            # Кто-то победил, надо обновить статусы
            winner_id = self.user_1_id if score_1 > score_2 else self.user_2_id
            loser_id = self.user_2_id if winner_id == self.user_1_id else self.user_1_id
            self.player_final_info[winner_id] = {"status": StatusEnum.WINNER.value, "diff": 10}
            self.player_final_info[loser_id] = {"status": StatusEnum.LOSER.value, "diff": -10}

    async def _update_scores(self, scores: dict):
        """Обновление счетчиков побед"""
        # Обновляем общие очки
        for pid, score in scores.items():
            self.scores[pid] += score

        self._update_statues()

        round_dto = RoundDTO(
            player_1=self.user_1_id,
            player_2=self.user_2_id,
            points_player_1=scores[self.user_1_id],
            points_player_2=scores[self.user_2_id],
            status_player_1=self.player_final_info[self.user_1_id]['status'],
            status_player_2=self.player_final_info[self.user_2_id]['status']
        )
        # создаем объект раунда в базе данных
        round_id = await self.round_service.create(round_dto)
        self.round_ids.append(round_id)

        # Отправка результатов раунда
        results = {
            "type": EventType.ROUND_RESULT.value,
            "scores": scores,
            "statuses": {
                self.user_1_id: self.player_final_info[self.user_1_id]['status'],
                self.user_2_id: self.player_final_info[self.user_2_id]['status']
            },
            "total_score": self.scores,
            "total_wins": self.wins
        }
        for ws in self.sockets.values():
            await ws.send_json(results)

    async def _get_final_msg(self, pid: str):
        """Сообщение с результатами игры"""
        return {
            "type": EventType.GAME_END.value,
            "status": self.player_final_info[pid]['status'],
            "diff": self.player_final_info[pid]['diff'],
            "new_rating": (await self.user_service.get_user(pid)).student_rating,
            "final_scores": self.scores
        }

    async def _end_game(self):
        """Обработка окончания игры"""
        self._update_statues()

        game_dto = NewGame(
            competition_id=self.competition_id,
            player_1=self.user_1_id,
            player_2=self.user_2_id,
            rounds=self.round_ids,
            status_player_1=self.player_final_info[self.user_1_id]['status'],
            status_player_2=self.player_final_info[self.user_2_id]['status'],
            rating_difference_player_1=self.player_final_info[self.user_1_id]['diff'],
            rating_difference_player_2=self.player_final_info[self.user_2_id]['diff'],
            score_player_1=self.scores[self.user_1_id],
            score_player_2=self.scores[self.user_2_id],
        )
        # Добавление статистики игры в базу данных
        await self.game_service.create_game(game_dto)
        await self._update_rating()
        # Отправка финальных результатов
        for pid, ws in self.sockets.items():
            msg = await self._get_final_msg(pid)
            await ws.send_json(msg)

    async def _update_rating(self):
        # Обновляем рейтинг
        for pid in self.players.keys():
            diff = self.player_final_info[pid]['diff']
            await self.user_service.update_student_rating(diff, pid)

