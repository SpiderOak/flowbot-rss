"""run.py - Run the RssBot."""

from bot import RssBot
from parse_feeds import RssFeedParser
from settings import settings
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='/src/bot.log', level=logging.DEBUG)
    bot = RssBot(settings)
    bot.run(block=False)
    try:
        parser = RssFeedParser(bot)
        parser.run()
    except (KeyboardInterrupt, SystemExit):
        bot.cleanup()
