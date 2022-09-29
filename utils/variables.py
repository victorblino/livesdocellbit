import os
from dotenv import load_dotenv
load_dotenv()

# Enviroment Variables
app_key = os.environ.get('TWITCH_APP_KEY')
app_secret = os.environ.get('TWITCH_APP_SECRET')
twitch_bearer = os.environ.get('TWITCH_TWITCH_BEARER')
streamer_nickname = os.environ.get('TWITCH_STREAMER_NICKNAME')
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
key = os.environ.get('TWITTER_KEY')
secret = os.environ.get('TWITTER_SECRET')
webhook_url = os.environ.get('WEBHOOK_URL')
port = os.environ.get('PORT', 8080)
bot_user = os.environ.get('TWITTER_BOT_NICKNAME')

# Variables Bot
games_played = list()
games_blacklist = ('Just Chatting', 'Tabletop Simulator', 'Watch Parties')

# Stream Variables
online: bool = False
title_stream = str 
category_name = str 
stream_id = int