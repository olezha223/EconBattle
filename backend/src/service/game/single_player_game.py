import asyncio

from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect

from src.models.game import EventType
from src.models.problems import TaskWithoutAnswers, TaskDTO
from src.models.users import UserData
from src.service import get_competition_service, get_task_service


class SinglePlayerGame:
    def __init__(
            self,
            user: UserData,
            websocket: WebSocket,
            competition_id: int
    ):
        self.user = user
        self.websocket = websocket
        self.competition_id = competition_id
        self.competition_service = get_competition_service()
        self.task_service = get_task_service()
        self.competition = None
        self.current_round = 0
        self.final_score = 0

    async def start(self):
        self.competition = await self.competition_service.get_competition(self.competition_id)
        try:
            await self.websocket.send_json(
                {
                    "type": "Game",
                    "msg": "Идет процесс игры",
                    "round_count": self.competition.max_rounds
                }
            )
            while self.current_round < self.competition.max_rounds:
                print(f"Начинаем раунд {self.current_round}")
                await self._start_round()
                self.current_round += 1
            await self._end_game()
        except asyncio.CancelledError:
            # Обработка прерывания игры
            print("Игра прервана")
        finally:
            print(f"Позвали клинап для одиночной игры {self.user}")
            await self._cleanup()

    async def _cleanup(self):
        if self.websocket and self.websocket.client_state == WebSocketState.CONNECTED:
            try:
                await self.websocket.send_json({"type": "Closing", "msg": f"{self.user.id} closing"})
                await self.websocket.close()
            except Exception as e:
                print(str(e))

    async def _get_problems_for_round(self) -> list[TaskWithoutAnswers]:
        tasks = [
            await self.task_service.get(task_id) for task_id in
            self.competition.tasks_markup[str(self.current_round + 1)].tasks
        ]
        return tasks


    async def _start_round(self):
        problems = await self._get_problems_for_round()
        time_limit = self.competition.tasks_markup[str(self.current_round + 1)].time_limit
        await self.websocket.send_json(
            {
                "type": "Start Round",
                "problems": [self.task_service.get_task_for_round(p).model_dump() for p in problems],
                "time_limit": time_limit - 10
            }
        )

        # Бэкенд ждет на 10 секунд дольше
        answers = await self._collect_answers(timeout=time_limit)

        print(answers)
        scores = self._calculate_scores(answers, problems)
        print(scores)
        await self._update_scores(scores)

    async def _collect_answers(self, timeout: int):
        task = asyncio.create_task(self._wait_for_answer(self.user.id, asyncio.Lock()))
        try:
            await asyncio.wait_for(task, timeout=timeout)
        except asyncio.TimeoutError:
            print("Время на ответы вышло")
            pass

        # Собираем результаты
        answer = None
        if task.done() and not task.cancelled():
            try:
                answer = task.result()
            except Exception as e:
                print("Неожиданная ошибкак при сборе результатов", str(e))
        else:
            task.cancel()
        return answer

    async def _wait_for_answer(self, player_id: int, lock: asyncio.Lock) -> tuple[int, list[int]]:
        """Ожидание ответа от конкретного игрока с блокировкой"""
        async with lock:
            try:
                if self.websocket.client_state == WebSocketState.CONNECTED:
                    data = await self.websocket.receive_json()
                    print(data, player_id)
                    return player_id, data.get("answers", [])
                return player_id, []
            except (WebSocketDisconnect, RuntimeError):
                return player_id, []

    @staticmethod
    def _calculate_scores(user_answer: dict, problems: list[TaskDTO]) -> int:
        """Расчет очков за раунд"""
        score = 0
        for problem in problems:
            problem_id = problem.id
            answer_list = user_answer.get(str(problem_id), None)
            if answer_list:
                if answer_list == problem.correct_value.get("answers", []):
                    score += problem.price
        return score

    async def _update_scores(self, score: int):
        self.final_score += score
        results = {
            "type": EventType.ROUND_RESULT.value,
            "score": score,
            "total_score": self.final_score,
        }
        await self.websocket.send_json(results)

    def _get_final_msg(self):
        return {
            "type": EventType.GAME_END.value,
            "final_scores": self.final_score
        }

    async def _end_game(self):
        await self.websocket.send_json(self._get_final_msg())