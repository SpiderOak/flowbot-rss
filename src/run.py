"""run.py - Run the RssBot."""

from bot import RssBot
from parse_feeds import RssFeedParser
from settings import settings


if __name__ == '__main__':
    bot = RssBot(settings)
    try:
        bot.run(block=False)
        parser = RssFeedParser(bot)
        parser.run()
    except (KeyboardInterrupt, SystemExit):
        bot.cleanup()
