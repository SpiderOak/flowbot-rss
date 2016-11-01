"""settings.py - Load the settings file into a python dict."""

import json

with open('settings.json') as data_file:
    _settings = json.load(data_file)

settings = _settings
