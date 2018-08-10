from unittest import TestCase

from aiounittest import AsyncTestCase
import asyncio
import os
from control4 import Control4


def get_proxy_url():
    if 'PROXY_URL' in os.environ:
        return os.environ['PROXY_URL']

    return None


def get_control4_url():
    # return 'http://10.12.44.28:9090/rest'

    if 'CONTROL4_URL' in os.environ:
        return os.environ['CONTROL4_URL']

    return 'http://10.0.1.95:8100/rest'


test_count = 100

stats = {'errors': 0, 'requests': 0}


class TestControl4(AsyncTestCase):
    def setUp(self):
        self._c4 = Control4(url=get_control4_url(), proxy=get_proxy_url())

    def tearDown(self):
        c4 = self._c4

        stats['errors'] += c4._stats['errors']
        stats['requests'] += c4._stats['requests']

        print('')
        print('')

        if c4._stats['requests'] > 0:
            print('================================ TEST RESULTS ================================')
            print('Requests: ', c4._stats['requests'])
            print('Errors: ', c4._stats['errors'])
            print('Rate: ', round(c4._stats['errors'] / c4._stats['requests'] * 100, 2), '%')
            print('')

        if stats['requests'] > 0:
            print('================================ TOTALS ================================')
            print('Total requests: ', stats['requests'])
            print('Total errors: ', stats['errors'])
            print('Total rate: ', round(stats['errors'] / stats['requests'] * 100, 2), '%')

    def test_can_instantiate(self):
        Control4(url=get_control4_url())

    async def test_get(self):
        c4 = self._c4

        result = await c4.get(12346, 9876)

        self.assertEqual(result, 'nil')

    async def test_issue_command(self):
        c4 = self._c4

        result = await c4.issue_command(123456, 'OFF')

        self.assertEqual(result, 'Command Issued')

    async def test_multiple_gets(self):
        c4 = self._c4

        for t in range(test_count):
            result = await c4.get(12346, 9876)
            self.assertEqual(result, 'nil')

        result = await c4.get(12346, 9876)

        self.assertEqual(result, 'nil')

    async def test_multiple_commands(self):
        c4 = self._c4

        for t in range(test_count):
            result = await c4.issue_command(123456, 'OFF')
            await asyncio.sleep(0.1)
            self.assertEqual(result, 'Command Issued')

    async def test_mixed_commands(self):
        c4 = self._c4

        for t in range(test_count):
            await c4.get(1112, 1000)
            await c4.issue_command(1112, 'OFF')
            await c4.issue_command(1112, 'ON')
            await asyncio.sleep(0.1)

    # async def test_issue_command_moo(self):
    #     c4 = self._c4
    #
    #     result = await c4.issue_command(1112, 'ON')
    #
    #     self.assertEqual(result, 'Command Issued')
