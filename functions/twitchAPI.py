import requests
import json

headers = {
    'Authorization': 'Bearer i21v12z4c2te3d5ebq064y0yc2dz6y',
    'Client-Id': 'g5zg0400k4vhrx2g6xi4hgveruamlv',
}

params = {
    'user_login': 'Cellbit',
}

def getStream():

    import datetime
    import dateutil.parser

    response = requests.get(
        'https://api.twitch.tv/helix/streams', params=params, headers=headers)
    responseText = response.text
    responseJson = json.loads(responseText)

    global started_at, game, vodId

    started_at = responseJson['data'][0]['started_at']
    game = responseJson['data'][0]['game_name']
    vodId = responseJson['data'][0]['id']
    title = responseJson['data'][0]['title']

    parsedDate = dateutil.parser.isoparse(started_at)
    parsedDate = str(parsedDate).split("+", 1)
    parsedDate = parsedDate[0]
    parsedDate = datetime.datetime.strptime(parsedDate, "%Y-%m-%d %H:%M:%S")

    now = datetime.datetime.now()
    now = str(now).split(".", 1)
    now = now[0]
    now = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

    diff = now - (parsedDate - datetime.timedelta(hours=0))

    seconds = diff.total_seconds()

    if seconds > 86400:
        tempo_no_vod = str(datetime.timedelta(seconds=seconds-86400))
        tempo_no_vod = datetime.datetime.strptime(tempo_no_vod, "%H:%M:%S")
        tempo_no_vod_hour = tempo_no_vod.hour + 24
        tempo_no_vod_minutes = tempo_no_vod.minute
        tempo_no_vod_seconds = tempo_no_vod.second

    else:
        tempo_no_vod = str(datetime.timedelta(seconds=seconds+86400, days=-1))
        tempo_no_vod = datetime.datetime.strptime(tempo_no_vod, "%H:%M:%S")
        tempo_no_vod_hour = tempo_no_vod.hour
        tempo_no_vod_minutes = tempo_no_vod.minute
        tempo_no_vod_seconds = tempo_no_vod.second

    return {
        'vodHours': tempo_no_vod_hour,
        'vodMinutes': tempo_no_vod_minutes,
        'vodSeconds': tempo_no_vod_seconds,
        'game': game,
        'vodId': vodId,
        'title': title,
        'started_at': started_at
    }

def isOnline():
    try:
        getStream()
        return True
    except:
        return False

def getImageGame(game):
    import urllib.request

    response = requests.get(
        f'https://api.twitch.tv/helix/games?name={game}', headers=headers)
    responseText = response.text
    responseJson = json.loads(responseText)
    
    imageUrl = responseJson['data'][0]['box_art_url'].replace('{width}', '600').replace('{height}', '800')

    urllib.request.urlretrieve(imageUrl, 'gameImg.jpg')


def getInfoUser():
    response = requests.get(
        f'https://api.twitch.tv/helix/users?login=Cellbit', params=params, headers=headers)
    responseText = response.text
    responseJson = json.loads(responseText)
    return {
        'userId': responseJson['data'][0]['id']
    } 

def getVideo():

    params = {
        'user_id': '28579002',
    }

    response = requests.get(
        f'https://api.twitch.tv/helix/videos?', headers=headers, params=params)
    responseText = response.text
    responseJson = json.loads(responseText)
    
    for videos in responseJson['data']:
        if videos['type'] == 'archive':
            link = videos['url']
            started_at = videos['created_at']
            return {
                'link': link,
                'started_at': started_at
            }

def dateStream():
    import datetime
    import dateutil.parser

    started_at = getVideo()['started_at']

    parsedDate = dateutil.parser.isoparse(started_at)
    parsedDate = str(parsedDate).split("+", 1)
    parsedDate = parsedDate[0]
    parsedDate = datetime.datetime.strptime(parsedDate, "%Y-%m-%d %H:%M:%S")

    return {
        'day': parsedDate.day,
        'month': parsedDate.month,
        'year': parsedDate.year
    }
