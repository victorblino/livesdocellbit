import tweepy
from utils import variables
from functions.botFunctions import printEvent

def connectTwitter():
    global api
    auth = tweepy.OAuthHandler(variables.consumer_key, variables.consumer_secret)
    auth.set_access_token(variables.key, variables.secret)
    api = tweepy.API(auth)
    printEvent(True, 'twitter_authenticated')
    return api

def postTweet(status):
    api.update_status(status)
    printEvent(True, 'twitter_post')

def postTweetWithImage(status, image):
    api.update_status_with_media(status, image)
    printEvent(True, 'twitter_post_image')

def postReply(status):
    last_tweet = api.user_timeline(screen_name=variables.bot_user)[0].id
    api.update_status(status, in_reply_to_status_id=last_tweet)
    printEvent(True, 'twitter_post_image')
