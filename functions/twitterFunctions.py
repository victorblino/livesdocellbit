import time
import tweepy
from utils import variables
from functions.botFunctions import printEvent


client = tweepy.Client(
    consumer_key=variables.consumer_key,
    consumer_secret=variables.consumer_secret,
    access_token=variables.twitter_access_token,
    access_token_secret=variables.twitter_access_secret,
    wait_on_rate_limit=True,
)

def _post(text: str, retries: int = 3, delay: int = 15) -> None:
    for attempt in range(retries):
        try:
            client.create_tweet(text=text)
            return
        except tweepy.errors.TwitterServerError:
            if attempt < retries - 1:
                printEvent(True, f'twitter_server_error_retry_{attempt + 1}')
                time.sleep(delay)
            else:
                raise

def postTweet(status: str) -> None:
    _post(status)
    printEvent(True, 'twitter_post')

def postTweetWithImage(status: str, image: str) -> None:
    _post(status)
    printEvent(True, 'twitter_post')
