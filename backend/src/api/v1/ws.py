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
        player_id: int = Query(..., alias="user_id", description="ID of the player"),
        competition_id: int = Query(..., alias="competition_id", description="ID of the competition")
):
    await websocket.accept()
    await websocket.send_json({"type": "connected", "msg": f"Игрок {player_id} подключен к серверу"})
    await match_maker.add_player(websocket, player_id, competition_id)
    print("вышло из игры для игрока", player_id)
