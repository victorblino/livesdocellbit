from utils import variables

def printEvent(sucessOrfail: bool, event: str, info: str='') -> None:
    colors = {
        True: '\33[92m',
        False: '\33[91m'
    }

    events = {
        # Bot

        'info_stream': '[BOT] Informações da Stream',
        'on_ready': '[BOT] ONLINE',

        # Twitch Authentication
        'twitch_authenticated': '[TWITCH AUTHENTICATION] OK',

        # Twitter Authenticaton
        'twitter_authenticated': '[TWITTER AUTHENTICATION] OK',

        # Twitter Posts 
        'twitter_post': '[TWITTER] POST SUCESSO',
        'twitter_post_image': '[TWITTER] POST IMAGE SUCESSO',
        'twitter_post_reply': '[TWITTER] POST REPLY SUCESSO',
        
        # Twitch Subscribe Event Subs
        'event_sub': '[EVENTSUB] OK',

        # Twitch Event Sub
        'live_on': '[TWITCH EVENTSUB] - Live Online!',
        'live_off': '[TWITCH EVENTSUB] - Live Offline',
        'game_changed': '[TWITCH EVENTSUB] - Game trocado - ',
        'title': '[TWITCH EVENTSUB] - Título trocado - '

    }

    return print(colors[sucessOrfail], events[event])

def downloadImageGame(image_url):
    from urllib.request import urlretrieve
    try:
        urlretrieve(image_url, 'imageGame.jpg')
    except:
        return False

def compareImages():
    from base64 import b64encode
    with open('404.jpg', 'rb') as not_found:
        image_not_found = b64encode(not_found.read())
    with open ('imageGame.jpg', 'rb') as game_image:
        image_game = b64encode(game_image.read())
        if image_not_found == image_game:
            return True
        return False

def gamesPlayed(games_list):
    games = ''
    for game in games_list: 
        games = f'• {game}\n'
    return games

def linkTwitchTracker(stream_id):
    return f'https://twitchtracker.com/{variables.streamer_nickname}/streams/{stream_id}'
