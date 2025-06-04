from typing import Any

from src.app.app import App
from src.config import configuration
from src.api.v1 import router_v1
from dataclasses import asdict


def main() -> Any:
    app: Any = App(
        host='localhost',
        port=8000,
        **asdict(configuration.app)
    ).included_cors(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ).included_routers(routers=[router_v1])
    return app
