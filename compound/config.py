import os
from typing import Type
from typing import Union

from compound.logger import get_logger
from compound.misc import log_and_raise

logger = get_logger(__name__)


class Config:
    validators = {
        str: lambda param: bool(param),
        int: lambda param: bool(param) and param.isnumeric(),
    }

    def __init__(self) -> None:
        self.api_url = self.get_param_str('API_URL')
        self.db_url = self.get_param_str('DB_URL')
        self.value_max_length = self.get_param_int('VALUE_MAX_LENGTH')

    def validate(self, name: str, value: str, type_: Union[Type[str], Type[int]]) -> None:
        if not self.validators[type_](value):
            log_and_raise(logger, f'Invalid environment variable value: {name}')

        logger.debug(f'Validated parameter: {name}:{value}')

    def get_param_str(self, name: str) -> str:
        param = os.getenv(name)
        self.validate(name, param, str)
        return param

    def get_param_int(self, name: str) -> int:
        param = os.getenv(name)
        self.validate(name, param, int)
        return int(param)
