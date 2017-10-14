import aiohttp
import asyncio
import contextlib
import emoji
import logging
from io import StringIO
import os
import pytest
from unittest.mock import Mock

import rssbot
from rssbot import bot, main, test_utils

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_default_answer(event_loop):
    async with test_utils.SandboxBot(event_loop, bot.Bot()) as sandbox:
        initial_history_length = len(sandbox.fb.history)
        await test_utils.post('http://0.0.0.0:{}/webhook'.format(os.environ.get('API_PORT', 8080)),
                              json={
                                  'object': 'page',
                                  'entry': [{
                                      'id': 'PAGE_ID',
                                      'time': 1458692752478,
                                      'messaging': [{
                                          'sender': {
                                              'id': 'USER_ID'
                                          },
                                          'recipient': {
                                              'id': 'PAGE_ID'
                                          },
                                          'timestamp': 1458692752478,
                                          'message': {
                                              'mid': 'mid.1457764197618:41d102a3e1ae206a38',
                                              'seq': 73,
                                              'text': 'hello, world!',
                                          }
                                      }]
                                  }]
                              })

        # use it because we spawn fb handler process and return 200Ok
        await asyncio.sleep(0.1)

        # we can't use initial_history_length + 1
        # because it is very likely that we don't have user USER_ID in our user's collection
        # and fb handler will ask user's profile meanwhile process income message

        assert len(sandbox.fb.history) > initial_history_length
        assert await sandbox.fb.history[-2]['request'].json() == {
            'message': {
                'text': emoji.emojize(
                    rssbot.SHORT_HELP.replace('{{user_first_name}}', 'friend'),
                    use_aliases=True,
                ),
            },
            'recipient': {'id': 'USER_ID'},
        }
        assert await sandbox.fb.history[-1]['request'].json() == {
            'message': {
                'text': 'For example: <give one random recommendation from bot + quick_replies>',
            },
            'recipient': {'id': 'USER_ID'},
        }
