from sre_constants import SUCCESS
from discord_webhook import DiscordWebhook # pyright: ignore
from base64 import b64encode

def compareImages():
        with open('./404.jpg', 'rb') as notFound:
            imageNotFound = b64encode(notFound.read())
        with open('gameImg.jpg', 'rb') as gameImage:
            img = b64encode(gameImage.read())
        if imageNotFound == img:
            return True
        else:
            return False

def sendWebhook(webhookUrl, message):
    webhook = DiscordWebhook(url=webhookUrl, rate_limit_retry=True, content=message)
    webhook.execute()

def printEvent(color, event):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m'
    }
    print(f'{colors[color]}{event}')