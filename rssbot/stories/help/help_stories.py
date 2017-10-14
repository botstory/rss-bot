import rssbot

from botstory.middlewares import any, option, sticker, text
from rssbot.utils import inject_first_name
import emoji
import logging

logger = logging.getLogger(__name__)


def setup(story):
    logger.debug('setup help stories')

    @story.on(receive=any.Any())
    def unhandled_message():
        @story.part()
        async def say_something(ctx):
            logger.warning('# Unhandled message')

            # TODO:
            # - store somewhere information about those messages
            # - add quick_replies

            help_msg = emoji.emojize(rssbot.SHORT_HELP, use_aliases=True)
            await story.say(
                inject_first_name(help_msg, ctx['user']),
                user=ctx['user']
            )

            await story.say(
                'For example: <give one random recommendation from bot + quick_replies>',
                user=ctx['user']
            )

            logger.debug('# end of say_something')
