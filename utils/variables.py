import os
from dotenv import load_dotenv
load_dotenv()

# Enviroment Variables
app_key = os.environ.get('TWITCH_APP_ID')
app_secret = os.environ.get('TWITCH_APP_SECRET')
streamer_nickname = os.environ.get('TARGET_USERNAME', '').capitalize()
webhook_url = os.environ.get('WEBHOOK_URL')
port = int(os.environ.get('PORT', 8080))
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_secret = os.environ.get('TWITTER_ACCESS_SECRET')

# Variables Bot
games_played = list()
games_blacklist = ('Just Chatting', 'Tabletop RPGs', 'Watch Parties')

# Stream Variables
online: bool = False
title_stream = str 
category_name = str 
stream_id = int
