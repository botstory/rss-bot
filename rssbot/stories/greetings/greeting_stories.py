import logging

import rssbot
from rssbot.utils import inject_first_name
# from rssbot.query import query_stories

logger = logging.getLogger(__name__)


def setup(story):
    @story.on_start()
    def on_start_story():
        @story.part()
        async def greet(ctx):
            await story.say(inject_first_name(rssbot.SHORT_INTO, ctx['user']),
                            user=ctx['user'])
            await story.say('For example: <give one random recommendation from bot + quick_replies>',
                            user=ctx['user'])
