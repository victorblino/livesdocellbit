import requests
import json

headers = {
    'Authorization': 'Bearer i21v12z4c2te3d5ebq064y0yc2dz6y',
    'Client-Id': 'g5zg0400k4vhrx2g6xi4hgveruamlv',
}

params = {
    'user_login': 'Cellbit',
}


def verifyGame():
    response = requests.get(
        'https://api.twitch.tv/helix/streams', params=params, headers=headers)
    responseText = response.text
    responseJson = json.loads(responseText)
    game = responseJson['data'][0]['game_name']
    return game


def isOnline():
    try:
        verifyGame()
        return True
    except:
        return False


def getImageGame(game):
    import urllib.request

    response = requests.get(
        f'https://api.twitch.tv/helix/games?name={game}', headers=headers)
    responseText = response.text
    responseJson = json.loads(responseText)
    imageUrl = responseJson['data'][0]['box_art_url'].replace(
        '{width}', '600').replace('{height}', '800')

    urllib.request.urlretrieve(imageUrl, 'gameImg.jpg')

def getProfileImage(user):
    response = requests.get(f'https://api.twitch.tv/helix/users?login={user} ', params=params, headers=headers)
    responseText = response.text
    responseJson = json.loads(responseText)
    print(responseJson)