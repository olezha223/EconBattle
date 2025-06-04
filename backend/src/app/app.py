from typing import Any

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


class App(FastAPI):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def included_routers(self, routers: list[APIRouter]) -> Any:
        for router in routers:
            self.include_router(router)

        return self

    def included_cors(
            self,
            allow_origins: list[str] | None = None,
            allow_credentials: bool | None = True,
            allow_methods: list[str] | None = None,
            allow_headers: list[str] | None = None
    ) -> Any:
        allow_origins = ['*'] if allow_origins is None else allow_origins
        allow_methods = ['*'] if allow_methods is None else allow_methods
        allow_headers = ['*'] if allow_headers is None else allow_headers

        self.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers
        )

        self.add_middleware(SessionMiddleware, secret_key="tunk-tunk-tunk-sahur", same_site="none")

        return self
