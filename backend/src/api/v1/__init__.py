from fastapi import APIRouter

from src.api.v1.auth import router_auth
from src.api.v1.competitions import router_competitions
from src.api.v1.games import router_games
from src.api.v1.tasks import router_problems
from src.api.v1.users import router_user
from src.api.v1.ws import ws_router


router_v1 = APIRouter()

router_v1.include_router(ws_router)
router_v1.include_router(router_problems)
router_v1.include_router(router_auth)
router_v1.include_router(router_competitions)
router_v1.include_router(router_user)
router_v1.include_router(router_games)