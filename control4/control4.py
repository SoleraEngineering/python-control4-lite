# -*- coding:utf-8 -*-

import requests


class Control4(object):
    def __init__(self, url):
        self._url = url
        self._session = requests.Session()

    def on(self, device_id):
        return self.issue_command(device_id, "ON")

    def off(self, device_id):
        return self.issue_command(device_id, "OFF")

    def set_level(self, device_id, level):
        return self.issue_command(device_id, "SET_LEVEL", {"LEVEL": level})

    def issue_command(self, device_id, command, params=None):
        if params is None:
            params = {}

        r = self._session.post(self._url, json={'command': command, 'deviceId': device_id, 'params': params})
        r.raise_for_status()
        return True

    def get(self, device_id, variable_id):
        r = self._session.get(self._url, params={'deviceid': device_id, 'variableid': variable_id})
        r.raise_for_status()
        return r.json()['variablevalue']
