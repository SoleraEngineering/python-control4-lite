# -*- coding:utf-8 -*-

import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)


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

        _LOGGER.debug('issue_command: cmd %s, device %d, params %s', command, device_id, str(params))
        async with aiohttp.ClientSession() as session:
            json_request = {'command': command, 'deviceId': device_id, 'params': params}

            async with session.post(self._url, json=json_request) as r:
                _LOGGER.debug('issue_command URL: %s', r.url)
                result = await r.json(content_type=None)
                _LOGGER.debug('issue_command response: %s', str(result))
                return result

    async def get(self, device_id, variable_id):
        _LOGGER.debug('get: device_id %d, variable_id %d', device_id, variable_id)

        async with aiohttp.ClientSession() as session:
            query_params = {'deviceid': device_id, 'variableid': variable_id}

            async with session.get(self._url, params=query_params) as r:
                _LOGGER.debug('get URL: %s', r.url)
                result = await r.json(content_type=None)
                _LOGGER.debug('get response: %s', str(result))
                return result['variablevalue']
