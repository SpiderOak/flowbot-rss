"""parse_feeds.py - Parse all feeds and message channels on new feed items."""
from rss_feed import RssFeed
import time


class RssFeedParser(object):
    """Parse all feed urls and message channels if new items are found."""

    def __init__(self, bot):
        """Initialize the parser by creating a connection to the RssBot."""
        self.bot = bot

    def run(self):
        """Loop through processing all feeds."""
        while True:
            self.process_all_feeds()
            time.sleep(60)

    def process_all_feeds(self):
        """Process new entries for all feeds in the queue."""
        for rss_feed in self._get_feed_queue():
            rss_feed.process_new_entries()

    def _get_feed_queue(self):
        """Return a list of RssFeed objects."""
        for feed_url, channels in self._load_feeds().items():
            yield RssFeed(feed_url, channels, self.bot)

    def _load_feeds(self):
        """Get all feed urls the list of channels to which they each belong."""
        feeds = {}
        for channel_id in self.bot.channels():
            channel_feeds = self.bot.get_feeds_for_channel(channel_id)
            for feed_url in channel_feeds:
                feeds.setdefault(feed_url, []).append(channel_id)
        return feeds
