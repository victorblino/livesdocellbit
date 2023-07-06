import tweepy
from utils import variables
from functions.botFunctions import printEvent


client = tweepy.Client(
    consumer_key=variables.consumer_key, consumer_secret=variables.consumer_secret,
    access_token=variables.twitter_access_token, access_token_secret=variables.twitter_access_secret
)

def postTweet(status):
    client.create_tweet(text=status)
    printEvent(True, 'twitter_post')

def postTweetWithImage(status, image):

    client.create_tweet(text=status)
    printEvent(True, 'twitter_post_image')

def postReply(status):

    last_tweet = client.user_timeline(screen_name=variables.bot_user)[0].id
    client.update_status(status, in_reply_to_status_id=last_tweet)
    printEvent(True, 'twitter_post_image')
