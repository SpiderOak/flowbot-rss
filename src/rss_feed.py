import feedparser
import redis
from datetime import datetime, timedelta
import os
from template_env import ENV


class RssFeed(object):
    """Implements feed parsing and Semaphor messaging for a given feed urls."""

    def __init__(self, feed_url, channels, bot):
        """Initialize feed object referencing the responsible flowbot."""
        self.bot = bot
        self.url = feed_url
        self.channels = channels
        self.redis = redis.StrictRedis(
            host=os.environ.get('REDIS_PORT_6379_TCP_ADDR'),
            port=6379
        )
        self.now = datetime.now()

    def process_new_entries(self):
        """Find all entries for this feed; send new entries to all channels."""
        feed_content = feedparser.parse(self.url)
        for entry in self._get_new_entries(feed_content):
            self._alert_channels_of_new_entry(entry)

    def _get_new_entries(self, feed_content):
        for entry in feed_content.get('entries', []):
            if self._is_new_entry(entry):
                yield entry
                self._mark_as_processed(entry)

    def _is_new_entry(self, entry):
        """Determine if this entry is new and should be processed."""
        entry_id = self._get_entry_id(entry)
        if not entry_id:
            return False

        if self._already_processed(entry_id):
            return False

        return self._is_entry_old(entry)

    def _is_entry_old(self, entry):
        """Determine if this entry should be considered "old"."""
        days_considered_old = 1
        published_date = self._entry_publised_datetime(entry)
        if published_date:
            age = self.now - published_date
            return age > timedelta(days=days_considered_old)
        return True

    def _entry_publised_datetime(self, entry):
        """Get the published datetime of the given entry."""
        published_time = entry.get('publshed_parsed')
        if published_time:
            return datetime(*published_time[0:6])
        return None

    def _already_processed(self, entry_id):
        """Determine if this entry has already been processed."""
        return self.redis.sismember(self.url, entry_id)

    def _mark_as_processed(self, entry):
        """Mark the given entry as "processed".

        Do this by adding the entry_id to a redis set for the parent feed.
        """
        entry_id = self._get_entry_id(entry)
        self.redis.sadd(self.url, entry_id)

    def _alert_channels_of_new_entry(self, entry):
        """Message all channels with a summary of the new entry."""
        for channel_id in self.channels:
            self.bot._render_to_channel(channel_id, 'new_entry.txt', {
                "entry": entry
            })

    @staticmethod
    def _get_entry_id(feed_entry):
        """Return a unique identifier for the entry.

        We use, "id" "guid" and "title" (in that order) for the unique
        identifier of a feed. If none of those keys exist, return None.
        """
        for identifier in ('id', 'guid', 'title'):
            value = feed_entry.get(identifier)
            if value:
                return value
        return None
