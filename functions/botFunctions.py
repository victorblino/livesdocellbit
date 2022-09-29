from utils import variables

def printEvent(sucessOrfail: bool, event: str) -> None:
    colors = {
        True: '\33[92m',
        False: '\33[91m'
    }

    events = {
        # Bot

        'info_stream': '[BOT] InformaÃ§Ãµes da Stream',
        'on_ready': '[BOT] ONLINE',

        # Twitch Authentication
        'twitch_authenticated': '[TWITCH AUTHENTICATION] OK',

        # Twitter Authenticaton
        'twitter_authenticated': '[TWITTER AUTHENTICATION] OK',
        
        # Twitch Subscribe Event Subs
        'subscribe': '[TWITCH EVENT SUB] - INICIANDO WEBHOOKS',
        'listen_online': '[TWITCH EVENTSUB] - LISTEN ONLINE!',
        'listen_offline': '[TWITCH EVENTSUB] - LISTEN OFFLINE',
        'listen_update': '[TWITCH EVENTSUB] - LISTEN UPDATES',

        # Twitch Event Sub
        'live_on': '[TWITCH EVENTSUB] - Live Online!',
        'live_off': '[TWITCH EVENTSUB] - Live Offline',
        'game_changed': '[TWITCH EVENTSUB] - Game trocado',
        'title': '[TWITCH EVENTSUB] - Título trocado'

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
    with open ('gameImage.jpg', 'rb') as game_image:
        image_game = b64encode(game_image.read())
        if image_not_found == image_game:
            return True
        return False

def gamesPlayed(games_list):
    games = ''
    for game in games_list: 
        games = f'{game}\n'
    return games 

def transformData(stream_timestamp):
    from datetime import datetime
    import dateutil.parser

    parsed_date = dateutil.parser.isoparse(stream_timestamp)
    parsed_date = str(parsed_date).split('+1', 1)
    parsed_date = parsed_date[0]
    parsed_date = datetime.strptime(parsed_date, '%Y-%m-%d %H:%M:%S')

    return f'[{parsed_date.day} {parsed_date.month} {parsed_date.year}]'

def linkTwitchTracker(stream_id):
    return f'https://twitchtracker.com/{variables.streamer_nickname}/streams/{stream_id}'
