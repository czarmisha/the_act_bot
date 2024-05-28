class SQLAlchemyRepo:
    def __init__(self, session):
        self._session = session
