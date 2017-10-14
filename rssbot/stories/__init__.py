from rssbot.stories.greetings import greeting_stories
from rssbot.stories.help import help_stories
from rssbot.stories.query import query_stories
from rssbot.stories.receive_feed import receive_feed_stories

story_modules = (
    greeting_stories,
    query_stories,

    # last hope :)
    # if we haven't handle message before,
    # then show help message to user
    help_stories,
)


def setup(story):
    for m in story_modules:
        m.setup(story)
