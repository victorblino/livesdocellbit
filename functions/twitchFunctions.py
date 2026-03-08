from twitchAPI.twitch import Twitch
from twitchAPI.eventsub.webhook import EventSubWebhook
from functions.botFunctions import compareImages, downloadImageGame, gamesPlayed, linkTwitchTracker, printEvent
from functions.twitterFunctions import postTweet, postTweetWithImage
from utils import variables
from random import choice

twitch = None

async def connectTwitch():
    global twitch
    twitch = await Twitch(variables.app_key, variables.app_secret)
    printEvent(True, 'twitch_authenticated')

async def connectEventSub():
    user_id = None
    async for user in twitch.get_users(logins=[variables.streamer_nickname]):
        user_id = user.id

    hook = EventSubWebhook(variables.webhook_url, variables.port, twitch)
    await hook.unsubscribe_all()
    hook.start()

    await hook.listen_stream_online(user_id, stream_online)
    await hook.listen_stream_offline(user_id, stream_offline)
    await hook.listen_channel_update(user_id, channel_update)
    printEvent(True, 'event_sub')
    return hook

async def verifyStreamIsOnline():
    try:
        user_id = None
        async for user in twitch.get_users(logins=[variables.streamer_nickname]):
            user_id = user.id

        found = False
        async for stream in twitch.get_streams(user_id=user_id):
            variables.title_stream = stream.title
            variables.category_name = stream.game_name
            variables.stream_id = stream.id
            found = True
            break

        if found:
            if variables.category_name not in variables.games_played and \
               variables.category_name not in variables.games_blacklist:
                variables.games_played.append(variables.category_name)
            variables.online = True
            printEvent(True, 'info_stream')
        else:
            variables.online = False

    except Exception:
        variables.online = False

async def stream_online(data):
    status = f'{variables.streamer_nickname} entrou ao vivo! {variables.title_stream}\n\ntwitch.tv/{variables.streamer_nickname}'
    try:
        postTweet(status)
        printEvent(True, 'live_on')
    except:
        try:
            postTweet(f'A stream provavelmente caiu, mas tá de volta -> twitch.tv/{variables.streamer_nickname}')
            printEvent(True, 'live_on')
        except:
            emoji = ('🌹', '✨', '🍎')
            postTweet(f'A stream provavelmente caiu, mas tá de volta -> twitch.tv/{variables.streamer_nickname} ({choice(emoji)}')
            printEvent(True, 'live_on')

    variables.online = True

async def stream_offline(data):
    from asyncio import sleep
    emoji = ('🌹', '✨', '🍎')
    status = f'{variables.streamer_nickname} encerrou a live!'

    try:
        postTweet(status)
        await sleep(1)
        printEvent(True, 'live_off')
    except:
        postTweet(f'{status} ({choice(emoji)})')
        printEvent(True, 'live_off')

    variables.online = False

async def channel_update(data):
    if variables.title_stream != data.event.title and variables.online is False:
        variables.title_stream = data.event.title
        postTweet(f'[TÍTULO] {variables.title_stream}')
        printEvent(True, 'title')

    if variables.category_name != data.event.category_name and variables.online is True:
        variables.category_name = data.event.category_name
        status = f'{variables.streamer_nickname} está jogando: {variables.category_name}\ntwitch.tv/{variables.streamer_nickname}'

        box_art_url = None
        async for game in twitch.get_games(names=[variables.category_name]):
            box_art_url = game.box_art_url.replace('{width}', '600').replace('{height}', '800')
            break

        if box_art_url:
            downloadImageGame(box_art_url)

        if variables.category_name not in variables.games_blacklist:
            variables.games_played.append(variables.category_name)

        if compareImages() is False and variables.category_name not in variables.games_blacklist:
            postTweetWithImage(status, 'imageGame.jpg')
        else:
            postTweet(status)
        printEvent(True, 'game_changed')
