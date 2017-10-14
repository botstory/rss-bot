import botstory
from botstory.integrations import aiohttp, fb, mongodb
from botstory.integrations.ga import tracker
import logging
import os

from rssbot import BOT_ID, BOT_NAME, GITHUB_URL, SHORT_INTO, stories


# TODO: here should be all documents
DOCUMENTS = ()

logger = logging.getLogger(BOT_NAME)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class Bot:
    def __init__(self):
        self.story = botstory.Story()

    def init(self, auto_start, fake_http_session):
        self.story.use(fb.FBInterface(
            # will show on initial screen
            greeting_text=SHORT_INTO,

            # you should get on admin panel for the Messenger Product in Token Generation section
            page_access_token=os.environ.get('FB_ACCESS_TOKEN', 'TEST_TOKEN'),
            # menu of the bot that user has access all the time
            persistent_menu=[
                {
                    'type': 'postback',
                    'title': 'Hi!',
                    'payload': 'ABOUT_ME',
                }, {
                    'type': 'nested',
                    'title': 'Help',
                    'call_to_actions': [
                        {
                            'type': 'web_url',
                            'title': 'Source Code',
                            'url': GITHUB_URL,
                        }, {
                            'type': 'postback',
                            'title': 'About',
                            'payload': 'ABOUT_ME',
                        },
                    ],
                },
            ],
            # should be the same as in admin panel for the Webhook Product
            webhook_url='/webhook{}'.format(os.environ.get('FB_WEBHOOK_URL_SECRET_PART', '')),
            webhook_token=os.environ.get('FB_WEBHOOK_TOKEN', None),
        ))

        # Interface for HTTP
        http = self.story.use(aiohttp.AioHttpInterface(
            port=int(os.environ.get('PORT', 8080)),
            auto_start=auto_start,
        ))

        # User and Session storage
        db = self.story.use(mongodb.MongodbInterface(
            uri=os.environ.get('MONGODB_URI', 'mongo'),
            db_name=os.environ.get('MONGODB_DB_NAME', BOT_ID),
        ))

        self.story.use(tracker.GAStatistics(
            tracking_id=os.environ.get('GA_ID'),
        ))

        # for test purpose
        http.session = fake_http_session

        stories.setup(self.story)
        return http, db

    async def setup(self, fake_http_session=None):
        logger.info('# setup')
        self.init(auto_start=False, fake_http_session=fake_http_session)
        await self.story.setup()

    async def start(self, auto_start=True, fake_http_session=None):
        logger.info('# start')
        http, db_integration = self.init(auto_start, fake_http_session)
        await self.story.setup()
        await self.story.start()
        for document in DOCUMENTS:
            document.setup(db_integration.db)
        return http.app

    async def stop(self):
        logger.info('# stop')
        await self.story.stop()
        self.story.clear()
