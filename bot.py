import os
import tweepy
import logging
import threading
from twitchAPI import Twitch, EventSub
from dotenv import load_dotenv
from functions.functionsBot import compareImages, sendWebhook
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
WEBHOOK_PDE = os.environ.get('WEBHOOK_PDE')

if LOGGING == 'TRUE':
    logging.basicConfig(level=logging.INFO)

# global variables
currentGame = None
currentTitle = None
streamId = None
online = False
gamesPlayed = list()
gamesBlacklist = ('Just Chatting', 'Watch Parties', 'Tabletop RPGs')
gamesTranslate = {
    'Just Chatting': 'Só na conversa',
    'Wordle': 'Raios Funde Letreco Musicle Posterdle Musicle Gamer'
}
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
    streamId = stream['data'][0]['id']
    if currentGame not in gamesBlacklist:
        gamesPlayed.append(currentGame)
    online = True
except:
    online = False

# functions callbacks
async def stream_online(data: dict):
    global online, currentGame, streamId
    stream = twitch.get_streams(user_id=user_id)
    title = stream['data'][0]['title']
    currentGame = stream['data'][0]['game_name']
    streamId = stream['data'][0]['id']
    api.update_status(f'Cellbit entrou ao vivo!\n\nTítulo: {title}\ntwitch.tv/cellbit')
    online = True

async def stream_offline(data: dict):
    global online, gamesPlayed
    api.update_status('Cellbit encerrou a live!')
    sendWebhook(WEBHOOK_PDE, 'Cellbit encerrou a live!')
    online = False

    if len(gamesPlayed) > 0:
        tweetId = api.user_timeline(screen_name='livesdocellbit')[0].id

        date = dateStream()
        status = f"[{date['day']}/{date['month']}/{date['year']}] Games Jogados:\n\n"
        for game in gamesPlayed:
            status += f'• {game}\n'
        status += f'\nVOD (Twitch Tracker): https://twitchtracker.com/cellbit/streams/{streamId}'
        api.update_status(status, in_reply_to_status_id = tweetId)
        gamesPlayed = list()

async def channel_update(data: dict):
    global currentGame, currentTitle, gamesPlayed

    game = data['event']['category_name']
    title = data['event']['title']

    if game != currentGame and online == True:
        # stream = twitch.get_streams(user_id=user_id)
        timeVod = getStream()
        h, m, s = timeVod['vodHours'], timeVod['vodMinutes'], timeVod['vodSeconds']
        try:
            import urllib.request
            imageUrl = twitch.get_games(names=game)['data'][0]['box_art_url'].replace('{width}', '600').replace('{height}', '800')
            urllib.request.urlretrieve(imageUrl, 'gameImg.jpg')
            if game not in gamesTranslate:
                status = f'Cellbit está jogando: {game}\nTempo no VOD: {h}h{m}m{s}s\n\ntwitch.tv/cellbit'
                sendWebhook(WEBHOOK_PDE, f'Cellbit está jogando {game}')
            else:
                status = f'Cellbit está jogando: {gamesTranslate[game]}\nTempo no VOD: {h}h{m}m{s}s\n\ntwitch.tv/cellbit'
                sendWebhook(WEBHOOK_PDE, f'Cellbit está jogando {gamesTranslate[game]}')

            if compareImages() or game in gamesBlacklist:
                api.update_status(status)
            elif game == 'Wordle':
                urllib.request.urlretrieve('https://i.imgur.com/IfcsMel.png', 'gameImg.jpg')
            else:
                api.update_status_with_media(status, 'gameImg.jpg')
        except:
            api.update_status(status)
        finally:
            if game not in gamesPlayed and game not in gamesBlacklist:
                gamesPlayed.append(game)
            currentGame = game

        # sleep(1)
        #  infoVideo = getVideo()        
    if title != currentTitle and online == False:
        api.update_status(f'[TÍTULO] {title}')
        sendWebhook(WEBHOOK_PDE, f'[TÍTULO] {title}')
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
