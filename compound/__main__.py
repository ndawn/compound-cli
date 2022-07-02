import sys
from argparse import ArgumentParser

from compound.cli import handler
from compound.config import Config
from compound.db.repository import Repository
from compound.db.session import SessionManager
from compound.logger import get_logger


argument_parser = ArgumentParser(prog='Compound CLI')
argument_parser.add_argument('command', help='Command to execute')
argument_parser.add_argument('arg', nargs='?', help='Command argument')

logger = get_logger(__name__)


def main(argv: list[str]) -> None:
    logger.debug('Reading command-line arguments')
    args = argument_parser.parse_args(argv)
    logger.debug(f'Read args: {args}')

    config = Config()
    session_manager = SessionManager(config)
    session = session_manager.get_session()
    repository = Repository(session)

    logger.debug('Entering session transaction')
    with session:
        session.begin()
        handler.configure(repository=repository, config=config, session=session)
        try:
            arg = args.arg.upper() if args.arg else None
            logger.debug(f'Handling {args.command} command with argument {arg}')
            handler.handle(args.command, arg)
            session.commit()
            logger.debug('Handling finished')
        except RuntimeError as exception:
            logger.error(f'An error occurred while executing handler: {exception}')
            session.rollback()


main(sys.argv[1:])
