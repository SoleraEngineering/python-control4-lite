from unittest import TestCase

from aiounittest import AsyncTestCase
import asyncio
import os
from control4 import Control4

def get_control4_url():
    return os.environ['CONTROL4_URL']


class TestControl4(AsyncTestCase):
    def test_can_instantiate(self):
        c4 = Control4(url=get_control4_url())

    async def test_get(self):
        c4 = Control4(url=get_control4_url())

        result = await c4.get(12346, 9876)

        self.assertEqual(result, 'nil')

    async def test_issue_command(self):
        c4 = Control4(url=get_control4_url())

        result = await c4.issue_command(123456, 'OFF')

        self.assertEqual(result, 'Command Issued')

    # async def test_issue_command_moo(self):
    #     c4 = Control4(url=get_control4_url())
    #
    #     result = await c4.issue_command(1112, 'ON')
    #
    #     self.assertEqual(result, 'Command Issued')
