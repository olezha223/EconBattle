from fastapi import WebSocket, APIRouter, Query
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
        competition_id: int = Query(..., alias="competition_id", description="ID of the competition")
):
    await websocket.accept()
    try:
        if match_maker.is_player_connected(player_id):
            await websocket.close(reason="Duplicate player")
            return
        await websocket.send_json({"type": "connected", "msg": f"Игрок {player_id} подключен"})
        await match_maker.add_player(websocket, player_id, competition_id)
    except WebSocketDisconnect:
        # Клиент сам отключился — сразу чистим
        match_maker.handle_disconnect(competition_id=competition_id, player_id=player_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Гарантированная очистка при отключении
        match_maker.handle_disconnect(competition_id=competition_id, player_id=player_id)
