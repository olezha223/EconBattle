from fastapi import FastAPI, WebSocket, APIRouter

from src.service.game.matchmaker import MatchMaker

ws_router = APIRouter()

match_maker = MatchMaker()


@ws_router.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await websocket.accept()
    await websocket.send_json({"type": "connected", "msg": f"Игрок {player_id} подключен к серверу"})
    try:
        await match_maker.add_player(websocket, player_id)
    except Exception as e:
        print(f'Упало с обычной ошибкой {player_id} \n {e}')
        try:
            await websocket.close()
        except RuntimeError:
            print(f"Упало с ошибкой, при этом закрыв соединение {player_id}")
