> Please Note: This project has not undergone a security review.

# flowbot-rss
A RSS bot for Semaphor!

## Running locally via Docker
Make sure you have docker installed and running locally before attempting to run this bot.

1. Download this code: `git clone https://github.com/SpiderOak/flowbot-rss.git`
2. Modify `src/settings.py` with your bot's specific settings
  - `username` is the username you'd like the bot to have
  - `password` the bot's password (Recovery Key), keep this safe.
  - `display_name` is the name that will show up in channels
  - `org_id` is the ID of the TEAM this bot will belong to
  - `photo` (optional) the filename of the image used for the bot's avatar
3. Run `make` from this directory.

## Example Usage

![watch](/doc/img/watch.png)

![list](/doc/img/list.png)

![help](/doc/img/help.png)