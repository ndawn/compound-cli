from typing import Any
from urllib.parse import urljoin

import requests

from compound.config import Config
from compound.db.models import CompoundType
from compound.logger import get_logger
from compound.misc import log_and_raise

logger = get_logger(__name__)


class ApiService:
    def __init__(self, config: Config) -> None:
        self.config = config

    def list_compounds(self, type_: CompoundType) -> list[dict[str, Any]]:
        url = urljoin(self.config.api_url, type_.value)

        logger.debug(f'Requesting {url}')
        response = requests.get(url)
        logger.debug(f'Received response with status code {response.status_code}')

        if 200 > response.status_code >= 300:
            log_and_raise(logger, 'Could not get a proper response from server')

        data = response.json()
        logger.debug(f'Data: {data}')
        return data.get(type_.value, [])
