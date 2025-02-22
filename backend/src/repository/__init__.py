from src.database.adapter import get_session


class RepoInterface:
    def __init__(self, session_getter=get_session):
        self.session_getter = session_getter
