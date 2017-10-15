from botstory.middlewares import any, option, sticker, text
import emoji
import logging

import rssbot
from rssbot.utils import is_url

logger = logging.getLogger(__name__)


def setup(story):
    logger.debug('setup receive feed stories')

    @story.on(text.Match(is_url.PATTERN))
    def url_message():
        @story.part()
        async def feed(ctx):
            logger.warning('# receive url')

            await story.say(
                'Thanks for link. '
                'I\'m going to define whether it feed or some resource',
                user=ctx['user'],
            )

            # It could be just link to regular article or link to feed

            # TODO:
            # - store somewhere information about those messages
            # - add quick_replies

            logger.debug('# end of say_something')
