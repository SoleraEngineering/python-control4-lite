# -*- coding:utf-8 -*-

import aiohttp
import logging
import time

_LOGGER = logging.getLogger(__name__)


class Control4RetryError(TimeoutError):
    pass


class Control4TimeoutError(TimeoutError):
    pass


def retry(times=10, timeout_secs=10):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            for t in range(times):
                try:
                    return await f(*args, **kwargs)
                except aiohttp.ClientResponseError as exc:
                    _LOGGER.debug('Received error response from Control4: %s', str(exc))

                    if timeout_secs is not None:
                        if time.time() - start_time > timeout_secs:
                            raise Control4TimeoutError()

            raise Control4RetryError
        return wrapper
    return func_wrapper


class Control4(object):
    def __init__(self, url):
        _LOGGER.debug('init: %s', url)
        self._url = url

    async def on(self, device_id):
        return await self.issue_command(device_id, "ON")

    async def off(self, device_id):
        return await self.issue_command(device_id, "OFF")

    async def set_level(self, device_id, level):
        return await self.issue_command(device_id, "SET_LEVEL", {"LEVEL": level})

    async def issue_command(self, device_id, command, params=None):
        if params is None:
            params = {}

        _LOGGER.debug('issue_command: cmd %s, device %d, params %s, url %s', command, device_id, str(params), self._url)

        json_request = {'command': command, 'deviceid': device_id, 'params': params}

        return await self._post_request(json_request)

    async def get(self, device_id, variable_id):
        _LOGGER.debug('get: device_id %d, variable_id %d', device_id, variable_id)

        query_params = {'deviceid': device_id, 'variableid': variable_id}

        return await self._get_request(query_params)

    @retry()
    async def _post_request(self, json_request):
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.post(self._url, json=json_request) as r:
                result = await r.text()
                _LOGGER.debug('issue_command response: (%d) %s', r.status, str(result))
                return result

    @retry()
    async def _get_request(self, query_params):
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(self._url, params=query_params) as r:
                result = await r.json(content_type=None)
                _LOGGER.debug('get response for (%s): (%d) %s', r.url, r.status, str(result))
                return result['variablevalue']

