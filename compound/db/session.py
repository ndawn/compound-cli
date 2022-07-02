from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from compound.config import Config
from compound.db.models import Base
from compound.logger import get_logger

logger = get_logger(__name__)


class SessionManager:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.engine = create_engine(self.config.db_url)
        self.session_class = sessionmaker(bind=self.engine)
        self._session_instance = None
        Base.metadata.create_all(self.engine)
        logger.debug(f'Initialized database schema')

    def get_session(self) -> Session:
        if self._session_instance is None:
            self._session_instance = self.session_class()

        return self._session_instance
