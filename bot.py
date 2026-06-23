import os
import tweepy
import logging
import threading
import requests
from twitchAPI import Twitch, EventSub
from dotenv import load_dotenv
from functions.functionsBot import compareImages
from functions.twitchAPI import getStream, dateStream, getVideo
from asyncio import sleep

# load env variables
load_dotenv()

# env variables 
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
APP_ID = os.environ.get('TWITCH_APP_ID')
APP_SECRET = os.environ.get('TWITCH_APP_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
PORT = os.environ.get('PORT', 8080)
TARGET_USERNAME = os.environ.get('TARGET_USERNAME')
LOGGING = os.environ.get('LOGGING')
POST_BACKEND = os.environ.get('POST_BACKEND', 'twitter').lower()
XQUIK_API_KEY = os.environ.get('XQUIK_API_KEY')
XQUIK_ACCOUNT = os.environ.get('XQUIK_ACCOUNT')
XQUIK_BASE_URL = os.environ.get('XQUIK_BASE_URL', 'https://xquik.com').rstrip('/')

if LOGGING == 'TRUE':
    logging.basicConfig(level=logging.INFO)

# global variables
currentGame = None
currentTitle = None
streamId = None
online = False
lastTweetId = None
gamesPlayed = list()
gamesBlacklist = ('Just Chatting', 'Watch Parties', 'Tabletop RPGs')
forever = threading.Event()

# login in twitch api
twitch = Twitch(APP_ID, APP_SECRET)
twitch.authenticate_app([])

api = None

def get_twitter_api():
    global api
    if api is not None:
        return api

    missing = list()
    for key, value in (
        ('TWITTER_CONSUMER_KEY', CONSUMER_KEY),
        ('TWITTER_CONSUMER_SECRET', CONSUMER_SECRET),
        ('TWITTER_ACCESS_TOKEN', ACCESS_TOKEN),
        ('TWITTER_ACCESS_SECRET', ACCESS_SECRET),
    ):
        if not value:
            missing.append(key)
    if missing:
        raise RuntimeError(f'Tweepy backend requires {", ".join(missing)}')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

if POST_BACKEND == 'xquik':
    print('Xquik text backend enabled')
else:
    try:
        get_twitter_api().verify_credentials()
        print('Authentication Successful')
    except:
        print('Authentication Error')

def post_with_xquik(status, in_reply_to_status_id=None):
    missing = list()
    if not XQUIK_API_KEY:
        missing.append('XQUIK_API_KEY')
    if not XQUIK_ACCOUNT:
        missing.append('XQUIK_ACCOUNT')
    if missing:
        raise RuntimeError(f'Xquik backend requires {", ".join(missing)}')

    payload = {
        'account': XQUIK_ACCOUNT,
        'text': status,
    }
    if in_reply_to_status_id is not None:
        payload['reply_to_tweet_id'] = str(in_reply_to_status_id)

    response = requests.post(
        f'{XQUIK_BASE_URL}/api/v1/x/tweets',
        headers={'x-api-key': XQUIK_API_KEY},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    return body.get('tweetId') or body.get('tweet_id')

def post_status(status, in_reply_to_status_id=None, media_path=None):
    if POST_BACKEND == 'xquik' and media_path is None:
        return post_with_xquik(status, in_reply_to_status_id)

    twitter_api = get_twitter_api()
    if media_path is not None:
        tweet = twitter_api.update_status_with_media(status, media_path)
    elif in_reply_to_status_id is not None:
        tweet = twitter_api.update_status(status, in_reply_to_status_id=in_reply_to_status_id)
    else:
        tweet = twitter_api.update_status(status)
    return getattr(tweet, 'id', None)

# get the user_id from twitch user
uid = twitch.get_users(logins=[TARGET_USERNAME])
user_id = uid['data'][0]['id']
currentTitle = twitch.get_channel_information(user_id)['data'][0]['title']

# get the informations
try:
    stream = twitch.get_streams(user_id=user_id)
    currentGame = stream['data'][0]['game_name']
    currentTitle = stream['data'][0]['title']
    streamId = stream['data'][0]['id']
    if currentGame not in gamesBlacklist:
        gamesPlayed.append(currentGame)
    online = True
except:
    online = False

# functions callbacks
async def stream_online(data: dict):
    global online, currentGame, streamId, lastTweetId
    stream = twitch.get_streams(user_id=user_id)
    title = stream['data'][0]['title']
    currentGame = stream['data'][0]['game_name']
    streamId = stream['data'][0]['id']
    lastTweetId = post_status(f'Cellbit entrou ao vivo!\n\nTítulo: {title}\ntwitch.tv/cellbit') or lastTweetId
    online = True

async def stream_offline(data: dict):
    global online, gamesPlayed, lastTweetId
    lastTweetId = post_status('Cellbit encerrou a live!') or lastTweetId
    online = False

    if len(gamesPlayed) > 0:
        tweetId = lastTweetId
        if POST_BACKEND != 'xquik':
            tweetId = get_twitter_api().user_timeline(screen_name='livesdocellbit')[0].id

        date = dateStream()
        status = f"[{date['day']}/{date['month']}/{date['year']}] Games Jogados:\n\n"
        for game in gamesPlayed:
            status += f'• {game}\n'
        if getVideo['title'] != currentTitle:
            status += f'\nVOD: https://twitchtracker.com/cellbit/streams/{streamId}'
        else:
            status += f'\nVOD: {getVideo()["link"]}'
        lastTweetId = post_status(status, in_reply_to_status_id=tweetId) or lastTweetId
        gamesPlayed = list()

async def channel_update(data: dict):
    global currentGame, currentTitle, gamesPlayed, lastTweetId

    game = data['event']['category_name']
    title = data['event']['title']

    if game != currentGame and online == True:
        # stream = twitch.get_streams(user_id=user_id)
        timeVod = getStream()
        h, m, s = timeVod['vodHours'], timeVod['vodMinutes'], timeVod['vodSeconds']
        status = f'Cellbit está jogando: {game}\nTempo no VOD: {h}h{m}m{s}s\n\ntwitch.tv/cellbit'
        try:
            import urllib.request
            imageUrl = twitch.get_games(names=game)['data'][0]['box_art_url'].replace('{width}', '600').replace('{height}', '800')
            urllib.request.urlretrieve(imageUrl, 'gameImg.jpg')
            if compareImages() or game == 'Just Chatting':
                lastTweetId = post_status(status) or lastTweetId
            else: 
                lastTweetId = post_status(status, media_path='gameImg.jpg') or lastTweetId
        except:
            lastTweetId = post_status(status) or lastTweetId
        finally:
            if game not in gamesPlayed and game not in gamesBlacklist:
                gamesPlayed.append(game)
            currentGame = game

        # sleep(1)
        #  infoVideo = getVideo()        
    if title != currentTitle and online == False:
        lastTweetId = post_status(f'[TÍTULO] {title}') or lastTweetId
        currentTitle = title

# subscribe to EventSub
hook = EventSub(WEBHOOK_URL, APP_ID, PORT, twitch)
hook.unsubscribe_all()
hook.start()

print('Iniciando webhooks...\n')

hook.listen_channel_update(user_id, channel_update)
print('[OK] CHANNEL UPDATE - WEBHOOK')
hook.listen_stream_offline(user_id, stream_offline)
print('[OK] STREAM OFFLINE - WEBHOOK')
hook.listen_stream_online(user_id, stream_online)
print('[OK] STREAM ONLINE - WEBHOOK')
print('\n')


try:
    print('Rodando!')
    forever.wait()
finally:
    hook.stop()
