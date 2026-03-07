import tweepy
from utils import variables
from functions.botFunctions import printEvent


client = tweepy.Client(
    consumer_key=variables.consumer_key,
    consumer_secret=variables.consumer_secret,
    access_token=variables.twitter_access_token,
    access_token_secret=variables.twitter_access_secret,
)

def postTweet(status: str) -> None:
    client.create_tweet(text=status)
    printEvent(True, 'twitter_post')

def postTweetWithImage(status: str, image: str) -> None:
    client.create_tweet(text=status)
    printEvent(True, 'twitter_post')
