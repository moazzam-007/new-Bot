# Telegram Deals Affiliate Bot
A Telegram bot that monitors deals channels, converts links to your affiliate links, and posts them to your channel.

## Features
- Monitors Telegram deals channels for new posts
- Converts product links to your affiliate links
- Amazon affiliate tag replacement
- Forwards modified messages to your channel

## Environment Variable


* `API_ID` - Get it from [mytelegram.org](https://my.telegram.org/auth). It's your Telegram application ID.
  
* `API_HASH` - Get it from [mytelegram.org](https://my.telegram.org/auth). It's your Telegram application hash.

* `BOT_TOKEN` - Get it from [@Botfather](https://t.me/botfather). It's the token for your Telegram bot.

* `PHONE_NUMBER` - Your phone number associated with the Telegram account.

* `MAIN_CHAT_ID` - The ID of the main chat where the bot will send messages (can be obtained from the bot).

* `STRING_SESSION` - The session string for your Pyrogram client. This can be generated using Pyrogram's `generate_string_session()` method.

* `CHANNELS` - A comma-separated list of channel IDs that the bot will monitor. For example: `123456789,987654321`.

* `FILTER_AMAZON_TAGS` - A comma-separated list of Amazon tags that the bot will use to filter Amazon deals.

* `YOUR_AMAZON_TAG` - Your Amazon affiliate tag is used to generate affiliate links.

* `EXTRAPE_SESSION_SECRET` - A secret session key for integrating with the Extrapé service for tracking.

* `LOG_GROUP_ID` - The Telegram group ID where logs of bot activity will be sent.


## Deploy to Heroku

You can quickly deploy this app to Heroku by clicking the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/iseshu/affiliate-bot)

## Running Locally

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with the variables above
4. Run: `python bot.py`


## Disclaimer
This bot is for educational purposes. Comply with Telegram's Terms of Service and Amazon Associates Program rules. Always disclose affiliate relationships.
