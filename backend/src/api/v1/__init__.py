from fastapi import APIRouter

from src.api.v1.ws import ws_router

router_v1 = APIRouter()

router_v1.include_router(ws_router)