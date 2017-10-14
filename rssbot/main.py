import asyncio
import argparse
import logging
from rssbot import bot
import sys


logger = logging.getLogger('main.py')
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


def setup():
    b = bot.Bot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(b.setup())


def start(forever=False):
    b = bot.Bot()
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(b.start(auto_start=forever))
    if forever:
        b.story.forever(loop)
    return app


def parse_args(args):
    parser = argparse.ArgumentParser(prog=bot.BOT_NAME)
    parser.add_argument('--setup', action='store_true', default=False, help='setup bot')
    parser.add_argument('--start', action='store_true', default=False, help='start bot')
    return parser.parse_args(args), parser


def main():
    parsed, parser = parse_args(sys.argv[1:])
    if parsed.setup:
        return setup()

    if parsed.start:
        return start(forever=True)

    parser.print_help()


if __name__ == '__main__':
    main()
