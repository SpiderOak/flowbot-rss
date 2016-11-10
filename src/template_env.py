"""template_env.py - Setting up the Jinja2 Template Environment."""

from jinja2 import Environment, FileSystemLoader
import os
import emoji


_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
ENV = Environment(loader=FileSystemLoader(_template_dir))


def emoji_filter(emoji_alias):
    """Return an emoji given the alias."""
    return emoji.emojize(emoji_alias, use_aliases=True)
ENV.filters['emoji'] = emoji_filter
