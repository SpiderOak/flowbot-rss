"""bot.py - an RSS Bot for Semaphor."""

from flowbot import FlowBot
from flowbot.decorators import mentioned
import re
from template_env import ENV


class RssBot(FlowBot):
    """Consume RSS feeds and post updates to Semaphor."""

    def commands(self):
        """Respond to the trigger words with the given function commands."""
        return {
            'unwatch': self.unwatch,
            'watch': self.watch,
            'list': self.list,
            'help': self.help
        }

    @mentioned
    def watch(self, flow_message):
        """Command bot to watch a RSS url in the current channel."""
        match = re.search(' watch (.*)', flow_message.get('text', ''))
        if match:
            feed = match.group(1)
            self._add_feed_to_channel(feed, flow_message['channelId'])
            self.reply(flow_message, 'Now watching %s in this channel' % feed)

    @mentioned
    def unwatch(self, flow_message):
        """Command bot to stop watching an RSS feed in the current channel."""
        match = re.search(' unwatch (\d+)', flow_message.get('text', ''))
        if match:
            channel_id = flow_message['channelId']
            idx = int(match.group(1)) - 1
            feeds = self.get_feeds_for_channel(channel_id)
            if idx < len(feeds):
                feed = feeds[idx]
                self._remove_feed_from_channel(feed, channel_id)
                self._render_response(flow_message, 'unwatch.txt', {
                    "url": feed,
                    "urls": self._get_indexed_feeds_for_channel(channel_id)
                })

    @mentioned
    def list(self, flow_message):
        """Command bot to list all RSS feeds watched in current channel."""
        channel_id = flow_message['channelId']
        self._render_response(flow_message, 'list.txt', {
            "urls": self._get_indexed_feeds_for_channel(channel_id),
            "botname": self.config.display_name
        })

    @mentioned
    def help(self, flow_message):
        """Command bot to show a help message."""
        self._render_response(flow_message, 'help.txt', {
            "botname": self.config.display_name
        })

    def get_feeds_for_channel(self, channel_id):
        """Return the list of feed urls followed in the given channel."""
        db_key = self._get_db_key('feeds', channel_id)
        feeds = self.channel_db.get_last(db_key)
        return feeds if feeds else []

    def _get_indexed_feeds_for_channel(self, channel_id):
        """Return a list of dicts containg in index and url value of feeds."""
        feeds = self.get_feeds_for_channel(channel_id)
        return [{"id": idx + 1, "url": url} for idx, url in enumerate(feeds)]

    def _render_response(self, orig_message, template_name, context={}, highlight=None):  # NOQA
        """Render the context to the message template and respond."""
        response = ENV.get_template(template_name)
        self.reply(orig_message, response.render(**context), highlight)

    def _render_to_channel(self, channel_id, template_name, context={}, highlight=None):  # NOQA
        """Render the context to the template and message the channel."""
        response = ENV.get_template(template_name)
        self.message_channel(channel_id, response.render(**context), highlight)

    def _add_feed_to_channel(self, feed_url, channel_id):
        """Add the feed_url to the list of watched feeds for the channel."""
        existing_feeds = self.get_feeds_for_channel(channel_id)
        if feed_url not in existing_feeds:
            existing_feeds.append(feed_url)
            self._update_channel_feeds(channel_id, existing_feeds)

    def _remove_feed_from_channel(self, feed_url, channel_id):
        """Remove the feed_url from the list of watched feeds."""
        existing_feeds = self.get_feeds_for_channel(channel_id)
        if feed_url in existing_feeds:
            existing_feeds.remove(feed_url)
            self._update_channel_feeds(channel_id, existing_feeds)

    def _update_channel_feeds(self, channel_id, feeds):
        """Update list of feeds followed in this channel."""
        db_key = self._get_db_key('feeds', channel_id)
        self.channel_db.new(db_key, feeds)

    def _get_db_key(self, keyname, channel_id):
        """Return the key used in the channel_db for the given channel_id."""
        return '%s_%s' % (keyname, channel_id)
