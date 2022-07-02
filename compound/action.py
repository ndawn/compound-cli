from abc import ABC
from abc import abstractmethod
from typing import Optional

from compound.config import Config
from compound.db.models import CompoundType
from compound.db.session import Session
from compound.db.repository import Repository
from compound.logger import get_logger
from compound.misc import log_and_raise

logger = get_logger(__name__)


class Action(ABC):
    def __init__(self, repository: Repository, config: Config, session: Session) -> None:
        self.repository = repository
        self.config = config
        self.session = session

    @abstractmethod
    def act(self, arg: Optional[str]) -> None:
        ...

    @staticmethod
    def _get_compound_enum_type(arg: Optional[str]) -> CompoundType:
        try:
            return CompoundType(arg)
        except ValueError:
            log_and_raise(logger, f'Unsupported compound type: {arg}')
