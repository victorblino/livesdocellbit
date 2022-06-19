import os
import tweepy
import logging
import threading
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

if LOGGING == 'TRUE':
    logging.basicConfig(level=logging.INFO)

# global variables
currentGame = None
currentTitle = None
online = False
gamesPlayed = list()
forever = threading.Event()

# login in twitch api
twitch = Twitch(APP_ID, APP_SECRET)
twitch.authenticate_app([])

# twitter authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print('Authentication Successful')
except:
    print('Authentication Error')

# get the user_id from twitch user
uid = twitch.get_users(logins=[TARGET_USERNAME])
user_id = uid['data'][0]['id']
currentTitle = twitch.get_channel_information(user_id)['data'][0]['title']

# get the informations
try:
    stream = twitch.get_streams(user_id=user_id)
    currentGame = stream['data'][0]['game_name']
    currentTitle = stream['data'][0]['title']
    online = True
except:
    online = False

# functions callbacks
async def stream_online(data: dict):
    global online, currentGame
    sleep(5)
    stream = twitch.get_streams(user_id=user_id)
    title = stream['data'][0]['title']
    currentGame = stream['data'][0]['game_name']
    api.update_status(f'Cellbit entrou ao vivo!\n\n {title}')
    online = True

async def stream_offline(data: dict):
    global online
    api.update_status('Cellbit encerrou a live!')
    online = False
    sleep(5)

    if len(gamesPlayed) > 0:
        try:
            date = dateStream()
        except:
            return
        status = f"[{date['day']}/{date['month']}/{date[year]}] Games Jogados:\n\n"
        for game in gamesPlayed:
            status += f'• {game}'
        status += f'VOD: {getVideo()["link"]}'
        tweetId = api.user_timeline(screen_name='livesdocellbit')[0].id
        api.update_status(status, in_reply_to_status_id = tweetId)
        return 

async def channel_update(data: dict):
    global currentGame, currentTitle, gamesPlayed

    game = data['event']['category_name']
    title = data['event']['title']

    if game != currentGame and online == True:
        stream = twitch.get_streams(user_id=user_id)
        timeVod = getStream()
        h, m, s = timeVod['vodHours'], timeVod['vodMinutes'], timeVod['vodSeconds']
        try:
            import urllib.request
            imageUrl = twitch.get_games(names=game)['data'][0]['box_art_url'].replace('{width}', '800').replace('{height}', '800')
            urllib.request.urlretrieve(imageUrl, 'gameImg.jpg')
            status = f'Cellbit está jogando {game}\nTempo no VOD: {h}h {m}m {s}s'
            if compareImages():
                api.update_status(f'Cellbit está jogando: {game}')
            else: 
                api.update_status_with_media(f'Cellbit está jogando: {game}\nTempo no VOD: {h}h {m}m {s}s', 'gameImg.jpg')
        except:
            api.update_status(f'Cellbit está jogando: {game}\nTempo no VOD: {h}h {m}m {s}s')
        finally:
            gamesBlacklist = ('Just Chatting', 'Watch Parties')
            if game not in gamesPlayed and game not in gamesBlacklist:
                gamesPlayed.append(game)
            currentGame = game

        sleep(3)
        link = getVideo()['link']
        tweetId = api.user_timeline(screen_name='livesdocellbit')[0].id
        api.update_status(f'Link do VOD: {link}?t={h}h{m}m{s}s', in_reply_to_status_id = tweetId)
        
    if title != currentTitle and online == False:
        api.update_status(f'[TÍTULO] {title}')
        currentTitle = title

# subscribe to EventSub
hook = EventSub(WEBHOOK_URL, APP_ID, PORT, twitch)
hook.unsubscribe_all()
hook.start()

print('Iniciando webhooks...\n')
try: 
    hook.listen_channel_update(user_id, channel_update)
    print('[OK] CHANNEL UPDATE - WEBHOOK')
    hook.listen_stream_offline(user_id, stream_offline)
    print('[OK] STREAM OFFLINE - WEBHOOK')
    hook.listen_stream_online(user_id, stream_online)
    print('[OK] STREAM ONLINE - WEBHOOK')
    print('\n')
except Exception as error:
    print(f'Erro! {error}')

try:
    forever.wait()
    print('Rodando!')
finally:
    hook.stop()