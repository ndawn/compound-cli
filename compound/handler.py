import logging
from typing import Callable
from typing import Type

from compound.action import Action
from compound.config import Config
from compound.db.repository import Repository
from compound.db.session import Session
from compound.logger import get_logger
from compound.misc import log_and_print
from compound.misc import log_and_raise

logger = get_logger(__name__)


class ActionHandler:
    def __init__(self) -> None:
        self.repository = None
        self.config = None
        self.session = None
        self._actions: dict[str, Type[Action]] = {}

    def action(self, command: str) -> Callable[[Type[Action]], Type[Action]]:
        def decorator(action: Type[Action]) -> Type[Action]:
            self.add_action(action, command)
            return action
        return decorator

    def add_action(self, action: Type[Action], command: str) -> None:
        self._actions[command] = action
        logger.debug(f'Registered action: {command}, {action}')

    def configure(self, repository: Repository, config: Config, session: Session) -> None:
        self.repository = repository
        self.config = config
        self.session = session

    def handle(self, command: str, arg: str) -> None:
        if None in (self.repository, self.session, self.config):
            log_and_raise(logger, 'Handler is not initialized yet')

        if command not in self._actions:
            log_and_print(
                logger,
                f'Unrecognized command: {command}. Available commands are: {", ".join(self._actions)}',
                logging.ERROR,
            )
            return

        action = self._actions[command](
            repository=self.repository,
            config=self.config,
            session=self.session,
        )

        action.act(arg)
