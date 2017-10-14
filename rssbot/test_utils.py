import logging
from botstory.integrations import aiohttp
from botstory.integrations.tests.fake_server import fake_fb

logger = logging.getLogger(__name__)


class SandboxBot:
    def __init__(self, event_loop, bot):
        self.bot = bot
        self.event_loop = event_loop
        self.fb = None
        self.session = None

    async def __aenter__(self):
        logger.debug('__aenter__')
        # nest fb server builder
        self.fb = fake_fb.FakeFacebook(self.event_loop)
        await self.fb.__aenter__()
        self.session = self.fb.session()
        await self.session.__aenter__()
        await self.bot.start(fake_http_session=self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.debug('__aexit__')
        logger.debug(exc_type)
        logger.debug(exc_val)
        logger.debug(exc_tb)
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
        await self.fb.__aexit__(exc_type, exc_val, exc_tb)
        await self.bot.stop()


async def post(url, json):
    http = aiohttp.AioHttpInterface()
    return await http.post_raw(url, json=json)
