from fastapi import FastAPI, WebSocket, APIRouter, Query

from src.service.game.matchmaker import MatchMaker

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
    if player_id in match_maker.manager.active_connections.keys():
        await websocket.accept()
        await websocket.close()
        return
    await websocket.accept()
    await websocket.send_json({"type": "connected", "msg": f"Игрок {player_id} подключен к серверу"})
    await match_maker.add_player(websocket, player_id, competition_id)
    print("вышло из игры для игрока", player_id)
