import logging

import aiohttp
from .rest_result import Result


class RestAdapter:
    def __init__(self,
                 hostname: str,
                 api_key: str,
                 ver: str,
                 content_type: str,
                 accept_language: str,
                 timeout: int = None,
                 retries: int = 0,
                 logger: logging.Logger = None):
        """

        @param hostname:        'https://enter.tochka.com/uapi/'
        @param api_key:         OAuth-token
        @param ver:             Api version
        @param content_type:    Content-type header
        @param accept_language: Accept-Language header
        @param timeout:         Timeout in second / None to request without timeout
        @param retries:         Additional attempt
        @param logger:          optional logger instance
        """
        self.hostname = f'https://{hostname}/{ver}'
        self.content_type = content_type
        self.accept_language = accept_language
        self._api_key = api_key
        self.ver = ver
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._retries = retries
        self._logger = logger or logging.getLogger(__package__)

    async def _do(self,
                  method: str,
                  endpoint: str,
                  params: dict[str, str] = None,
                  payload: dict = None) -> Result:
        """

        @param method:      GET, POST, DELETE
        @param endpoint:    URL endpoint
        @param params:      Params
        @param payload:     Dictionary with payload
        @return: Result instance
        """


