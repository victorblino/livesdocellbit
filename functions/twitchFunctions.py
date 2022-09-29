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
            return variables.category_name

    except IndexError:  # Stream offline
        variables.online = False
        return variables.online 

async def stream_online(data: dict):
    emoji = ('â˜•', 'ðŸ§›', 'ðŸ‘¾')
    variables.title_stream = data['event']['title']
    status = f'{variables.streamer_nickname} entrou ao vivo! {variables.title_stream}\n\ntwitch.tv/{variables.streamer_nickname}'
    try:
        postTweet(status)
    except: # If error (tweet is same)
        postTweet(f'{status} ({choice(emoji)})')

async def stream_offline(data: dict):
    emoji = ('â˜•', 'ðŸ§›', 'ðŸ‘¾')
    status = f'{variables.streamer_nickname} encerrou a live!'
    status_games_played = f'Games Jogados\n{gamesPlayed(variables.games_played)}\nVOD: {linkTwitchTracker(variables.stream_id)}'
    
    try:
        postTweet(status)
        await sleep(1)
        postReply(status_games_played)
    except:
        postTweet(f'{status} ({choice(emoji)})')

async def channel_update(data: dict):

    id_streamer = twitch.get_users(logins=[variables.streamer_nickname])['data'][0]['id']

    if variables.title_stream == data['event']['title'] and variables.online is False: # If title change and stream is offline
        variables.title_stream = data['event']['title'] # Set variable new title
        status = f'[TÃTULO] {variables.title_stream}'
        postTweet(status)

    elif variables.category_name != data['event']['category_name'] and variables.online == True: # If category (or game) change
        
        timestamp = twitch.get_videos(user_id=id_streamer)['data'][0]['duration'] # Get timestamp in VOD
        variables.category_name = data['event']['category_name'] # Change the game variable
        variables.games_played.append(variables.category_name)
        status = f'{variables.streamer_nickname} estÃ¡ jogando: {variables.category_name}\nTempo no VOD: {timestamp}\n\ntwitch.tv/{variables.streamer_nickname}' # Prepare Twitter status
        downloadImageGame(twitch.get_games(names=variables.category_name)['data'][0]['box_art_url'].replace('{width}', '600').replace('{height}', '800')) # Download image game

        if compareImages() is False: # Verify if image game is equal a 404 image
            postTweetWithImage(status, 'imageGame.jpg')
            return
        else:
            postTweet(status)
            return