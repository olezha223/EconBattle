from fastapi import WebSocket, APIRouter, Query, Depends, HTTPException
from starlette import status

from src.service import UserService, get_user_service, CompetitionService, get_competition_service
from src.service.game.matchmaker import MatchMaker
from starlette.websockets import WebSocketDisconnect

ws_router = APIRouter(
    prefix="/ws",
    tags=["WS"],
)

match_maker = MatchMaker()


@ws_router.websocket("/")
async def websocket_endpoint(
        websocket: WebSocket,
        player_id: str = Query(..., alias="user_id", description="ID of the player"),
        competition_id: int = Query(..., alias="competition_id", description="ID of the competition"),
        user_service: UserService = Depends(get_user_service),
        competition_service: CompetitionService = Depends(get_competition_service),
):
    await websocket.accept()
    user = await user_service.get_user(player_id)
    if not user:
        # если такого игрока не существует, необходимо закрыть соединение с кодом 404
        await websocket.close(code=status.HTTP_404_NOT_FOUND)
        return

    competition = await competition_service.get_competition(competition_id)
    if not competition:
        # если такого соревнования не существует, необходимо закрыть соединение с кодом 404
        await websocket.close(code=status.HTTP_404_NOT_FOUND)
        return

    try:
        if match_maker.is_player_connected(player_id):
            # если игрок еще не отключился, нельзя давать ему играть вторую игру одновременно
            await websocket.close(reason="Duplicate player")
            return
        # после всех проверок можно сообщить игроку, что он успешно подключен к серверу и ждет соперника
        await websocket.send_json({"type": "connected", "msg": f"Игрок {player_id} подключен"})
        # добавляем в очередь сообщений
        await match_maker.add_player(websocket, player_id, competition_id)
    except WebSocketDisconnect:
        # Клиент сам отключился — сразу чистим
        match_maker.handle_disconnect(competition_id=competition_id, player_id=player_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Гарантированная очистка при отключении
        match_maker.handle_disconnect(competition_id=competition_id, player_id=player_id)
