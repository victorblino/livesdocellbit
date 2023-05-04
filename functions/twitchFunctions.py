from twitchAPI import Twitch, EventSub
from functions.botFunctions import compareImages, downloadImageGame, gamesPlayed, linkTwitchTracker, printEvent
from functions.twitterFunctions import postReply, postTweet, postTweetWithImage
from utils import variables
from asyncio import sleep
from random import choice

def connectTwitch():
    global twitch
    twitch = Twitch(variables.app_key, variables.app_secret)
    twitch.authenticate_app([])  # Authenticate the app
    printEvent(True, 'twitch_authenticated')

def connectEventSub():
    id_streamer = twitch.get_users(logins=[variables.streamer_nickname])['data'][0]['id']

    # Subscribe in Event Subs
    hook = EventSub(variables.webhook_url, variables.app_key, variables.port, twitch)
    hook.unsubscribe_all()  # Unsubscribe to prevent bugs
    hook.start()

    hook.listen_stream_online(id_streamer, stream_online)
    hook.listen_stream_offline(id_streamer, stream_offline)
    hook.listen_channel_update(id_streamer, channel_update)
    printEvent(True, 'event_sub')
    return hook

def verifyStreamIsOnline():
    # Verify if stream is online
    try:
        global stream
        id_streamer = twitch.get_users(logins=[variables.streamer_nickname])['data'][0]['id']
        stream_info = twitch.get_streams(user_id=id_streamer)['data'][0]
        variables.title_stream, variables.category_name, variables.stream_id = stream_info['title'], stream_info['game_name'], stream_info['id']
        printEvent(True, 'info_stream')      
        # If game not in games played add in list
        if variables.category_name not in variables.games_played and variables.category_name not in variables.games_blacklist:
            variables.games_played.append(variables.category_name)
            variables.online = True
            return

    except IndexError:  # Stream offline
        variables.online = False
        return 

async def stream_online(data: dict):
    emoji = ('🌹', '✨', '🍎')
    status = f'{variables.streamer_nickname} entrou ao vivo! {variables.title_stream}\n\ntwitch.tv/{variables.streamer_nickname}'
    try:
        postTweet(status)
        printEvent(True, 'live_on')
    except: # If error (tweet is same)
        postTweet(f'A stream provavelmente caiu, mas tá de volta -> twitch.tv/{variables.streamer_nickname})')
        printEvent(True, 'live_on')

    variables.online = True

async def stream_offline(data: dict):
    emoji = ('🌹', '✨', '🍎')
    status = f'{variables.streamer_nickname} encerrou a live!'
    status_games_played = f'Para ter acesso a stream e jogos jogados, acesse: {linkTwitchTracker(str(variables.stream_id))}'
    
    try:
        postTweet(status)
        await sleep(1)
        postReply(status_games_played)
        printEvent(True, 'live_off')
    except:
        postTweet(f'{status} ({choice(emoji)})')
        postReply(status_games_played)
        printEvent(True, 'live_off')

    variables.online = False

async def channel_update(data: dict):

    id_streamer = twitch.get_users(logins=[variables.streamer_nickname])['data'][0]['id']

    if variables.title_stream != data['event']['title'] and variables.online is False: # If title change and stream is offline
        variables.title_stream = data['event']['title'] # Set variable new title
        status = f'[TÍTULO] {variables.title_stream}'
        postTweet(status)
        printEvent(True, 'title')

    if variables.category_name != data['event']['category_name'] and variables.online == True: # If category (or game) change
        
        if variables.title_stream == twitch.get_videos(user_id=id_streamer)['data'][0]['duration']:
            timestamp = twitch.get_videos(user_id=id_streamer)['data'][0]['duration'] # Get timestamp in VOD
            status = f'{variables.streamer_nickname} está jogando: {variables.category_name}\nTempo no VOD: {timestamp}\n\ntwitch.tv/{variables.streamer_nickname}' # Prepare Twitter status
        else: 
            status = f'{variables.streamer_nickname} está jogando: {variables.category_name}\n\ntwitch.tv/{variables.streamer_nickname}' # Prepare Twitter status
        variables.category_name = data['event']['category_name'] # Change the game variable
        
        downloadImageGame(twitch.get_games(names=variables.category_name)['data'][0]['box_art_url'].replace('{width}', '600').replace('{height}', '800')) # Download image game

        if variables.category_name not in variables.games_blacklist: # Add game in list
            variables.games_played.append(variables.category_name)

        if compareImages() is False and variables.category_name not in variables.games_blacklist: # Verify if image game is equal a 404 image
            postTweetWithImage(status, 'imageGame.jpg')
            printEvent(True, 'game_changed')
            return
        else:
            postTweet(status)
            printEvent(True, 'game_changed')
            return
