from botstory.middlewares import any, option, sticker, text
from botstory.integrations import commonhttp
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
            logger.info('# receive url')

            await story.say(
                'Thanks for the link. '
                'I\'m going to define whether it feed or something else.',
                user=ctx['user'],
            )

            await story.start_typing(
                user=ctx['user'],
            )

            uri = text.get_raw_text(ctx)
            d = feedparser.parse(uri)
            d.bozo  # does it have problems
            try:
                org_href = d.href  # link to the original page
                link = d.feed.link  # looks the same

                title = d['feed']['title']
                subtitle = d.feed.subtitle  # more information about feed
                summary = d.feed.subtitle  # more information about feed
                author = d.feed.author
                authors = d.feed.author
                # [{'email': 'TheTalkingMachines@gmail.com',
                #   'name': 'Katherine Gorman'},
                #  {'name': 'Tote Bag Productions'}]
                img_url = d.feed.image.href  # optional
                lang = d.feed.language
                tags = d.feed.tags
                # [{'label': None,
                #   'scheme': 'http://www.itunes.com/',
                #   'term': 'Technology'},
                #  {'label': None,
                #   'scheme': 'http://www.itunes.com/',
                #   'term': 'Tech News'},

                #
                # Do not yet decided which way is better to reflect feed
                #
                # await story.say(
                #     'Feed: {} by {}'.format(title, author),
                #     user=ctx['user']
                # )
                #
                # await story.send_image(
                #     img_url,
                #     user=ctx['user']
                # )

                await story.send_template(
                    payload={
                        'template_type': 'generic',
                        'elements': [
                            {
                                'title': 'Feed: {} by {}'.format(title, author),
                                'image_url': img_url,
                                'subtitle': summary,
                                # 'default_action': {
                                #     'type': 'web_url',
                                #     'url': link,
                                # },
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': link,
                                        'title': 'Website'
                                    }
                                ]
                            }
                        ]
                    },
                    user=ctx['user'],
                )

                for entry in d.entries:
                    # entry.id #UID

                    try:
                        href = entry.image.href
                        await story.start_typing(
                            user=ctx['user'],
                        )
                        await story.send_image(href,
                                               user=ctx['user'])
                    except AttributeError:
                        pass

                    await story.say(
                        emoji.emojize(':star: {}'.format(entry.title), use_aliases=True),
                        user=ctx['user'],
                    )

                    # entry.title # name of entity / 'Childhood Obesity'
                    # entry.subtitle # could be the same as title
                    # entry.summary # full message
                    # entry.content # the same as summary but in different style
                    # Example:
                    # [{'base': 'https://rss.art19.com/talking-machines',
                    #   'language': None,
                    #   'type': 'text/plain',
                    #   'value': 'In episode ten of season three we talk about the rate '
                    #            'of change (prompted by Tim Harford), take a listener '
                    #            'question about the power of kernels, and talk with '
                    #            'Peter Donnelly in his capacity with the Royal '
                    #            "Society's Machine Learning Working Group about the "
                    #            "work they've done on the public's views on AI and ML."},
                    #  {'base': 'https://rss.art19.com/talking-machines',
                    #   'language': None,
                    #   'type': 'text/html',
                    #   'value': '<p>In episode ten of season three we talk about the '
                    #            'rate of change <a '
                    #            'href="http://www.bbc.com/news/business-40673694" '
                    #            'target="_blank">(prompted by Tim Harford)</a>, take a '
                    #            'listener question about the power of kernels, and talk '
                    #            'with <a '
                    #            'href="https://royalsociety.org/people/peter-donnelly-11348/" '
                    #            'target="_blank">Peter Donnelly</a> in his capacity '
                    #            'with the <a '
                    #            'href="https://royalsociety.org/about-us/committees/machine-learning-working-group/" '
                    #            'target="_blank">Royal Society\'s Machine Learning '
                    #            "Working Group</a> about the work they've done on the "
                    #            '<a '
                    #            'href="https://royalsociety.org/~/media/policy/projects/machine-learning/publications/machine-learning-report.pdf" '
                    #            'target="_blank">public\'s views on AI and ML</a>. '
                    #            '</p>'}]
                    # entry.link # url to get more
                    # entry.published # when it was published
                    # entry.image.href # could have image optional
                    # entry.itunes_duration
                    # Example:
                    # 00:44:12
                    # entry.tags # could have tags the same as d.tags
                    # entry.links
                    # Example:
                    # [{
                    #      'href': 'http://open.live.bbc.co.uk/mediaselector/5/redir/version/2.0/mediaset/audio-nondrm-download-low/proto/http/vpid/p05jw1j9.mp3',
                    #      'length': '23984000',
                    #      'rel': 'enclosure',
                    #      'type': 'audio/mpeg'},
                    #  {'href': 'http://www.bbc.co.uk/programmes/w3csv1fd',
                    #   'rel': 'alternate',
                    #   'type': 'text/html'}]
                    for entry_link in entry.links:
                        if entry_link.type == 'audio/mpeg':
                            # TODO: publish audio file
                            # entry_link.length
                            logger.debug('[!] before publish {}'.format(entry_link.href))
                            try:
                                await story.start_typing(
                                    user=ctx['user'],
                                )

                                await story.send_audio(url=entry_link.href,
                                                       user=ctx['user'])
                            except commonhttp.errors.HttpRequestError as err:
                                logger.error('failed on podcast uploading ({}) upload {}'.format(entry_link.href, err))
                                await story.say(
                                    emoji.emojize(':hear_no_evil: failed on podcast uploading. Could retry later...',
                                                  use_aliases=True),
                                    user=ctx['user'],
                                )

                                # entry.media_content # optional, but could be link
                                # Example:
                                # [{'duration': '2998',
                                #   'expression': 'full',
                                #   'filesize': '23984000',
                                #   'medium': 'audio',
                                #   'type': 'audio/mpeg',
                                #   'url': 'http://open.live.bbc.co.uk/mediaselector/5/redir/version/2.0/mediaset/audio-nondrm-download-low/proto/http/vpid/p05jw1j9.mp3'}],
                                # for media_content in entry.media_content:
                                #     if media_content.type == 'audio/mpeg':
                                #         # publish audio file
                                #         media_content.url
                                #         # for link
                                #         media_content.href

            except AttributeError as e:
                logger.warning(e)

            await story.stop_typing(
                user=ctx['user'],
            )

            # It could be just link to regular article or link to feed

            # TODO:
            # - store somewhere information about those messages
            # - add quick_replies

            logger.debug('# end of say_something')
