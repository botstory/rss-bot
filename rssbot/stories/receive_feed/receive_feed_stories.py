from botstory.middlewares import any, option, sticker, text
import emoji
import feedparser
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

            uri = text.get_raw_text(ctx)
            d = feedparser.parse(uri)
            try:
                org_href = d.href
                title = d['feed']['title']
                subtitle = d.feed.subtitle
                author = d.feed.author
                img_url = d.feed.image.href
                lang = d.feed.language
                tags = d.feed.tags

                await story.say(
                    'Feed: {} by '.format(title, author),
                    user=ctx['user']
                )

                await story.send_image(
                    img_url,
                    user=ctx['user']
                )

                for entry in d.entries:
                    entry.id #UID
                    entry.title # name of entity / 'Childhood Obesity'
                    entry.subtitle # could be the same as title
                    entry.summary # full message
                    entry.link # url to get more
                    entry.published # when it was published
                    entry.links
                    # [{
                    #      'href': 'http://open.live.bbc.co.uk/mediaselector/5/redir/version/2.0/mediaset/audio-nondrm-download-low/proto/http/vpid/p05jw1j9.mp3',
                    #      'length': '23984000',
                    #      'rel': 'enclosure',
                    #      'type': 'audio/mpeg'},
                    #  {'href': 'http://www.bbc.co.uk/programmes/w3csv1fd',
                    #   'rel': 'alternate',
                    #   'type': 'text/html'}]
                    entry.media_content
                    # [{'duration': '2998',
                    #   'expression': 'full',
                    #   'filesize': '23984000',
                    #   'medium': 'audio',
                    #   'type': 'audio/mpeg',
                    #   'url': 'http://open.live.bbc.co.uk/mediaselector/5/redir/version/2.0/mediaset/audio-nondrm-download-low/proto/http/vpid/p05jw1j9.mp3'}],
                    for media_content in entry.media_content:
                        if media_content.medium == 'audio/mpeg':
                            # publish audio file
                            media_content.url

            except AttributeError as e:
                logger.debug(e)

            # It could be just link to regular article or link to feed

            # TODO:
            # - store somewhere information about those messages
            # - add quick_replies

            logger.debug('# end of say_something')
