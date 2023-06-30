import tweepy
from utils import variables
from functions.botFunctions import printEvent

def connectTwitter():
    global api
    api = tweepy.Client(
        consumer_key=variables.consumer_key, consumer_secret=variables.consumer_secret,
        access_token=variables.app_key, access_token_secret=variables.secret
    )
    printEvent(True, 'twitter_authenticated')
    return api

def postTweet(status):
    api.create_tweet(text=status)
    printEvent(True, 'twitter_post')

def postTweetWithImage(status, image):
    api.create_tweet(text=status)
    printEvent(True, 'twitter_post_image')

def postReply(status):
    last_tweet = api.user_timeline(screen_name=variables.bot_user)[0].id
    api.update_status(status, in_reply_to_status_id=last_tweet)
    printEvent(True, 'twitter_post_image')
