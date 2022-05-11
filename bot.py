from functions.twitchAPI import getStream, isOnline, getImageGame, getVideo, dateStream
from functions.functionsBot import compareImages

import os
from time import sleep

import discord
from discord.ext import tasks

import tweepy

global currentGame, online, gamesPlayed
gamesPlayed = list()

auth = tweepy.OAuthHandler("GPRorX0IZ7wp4s9EcmD1Y3Vzp", "icHW0EvWkmbPXZUoukUZY2ow9BAeiGvKrMwdWm9zlZiNJ926z7")
auth.set_access_token("1278567210991210502-sEmyQXOYI4HMPBHxYP2MEzo9RKKGuQ", "o4uhnyVCnuq5INQc3EqGpLEeGvf5JaJPzdgjtuURwCvZY")
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication Successful")
except:
    print("Authentication Error")

online = False
currentGame = None
bot = discord.Bot()

if isOnline():
    online = True
    currentGame = getStream()['game']

@bot.event
async def on_ready():
    print('Online!')
    checkGame.start()


@tasks.loop(seconds=15)
async def checkGame():
    global online
    
    if isOnline() == True and online == False:
        try: 
            title = getStream()['title']
        except Exception as err: 
            print(f'Erro na função isOnline: {err}')
            return
        api.update_status(f'Cellbit entrou ao vivo!\nTítulo: {title}\nhttps://twitch.tv/cellbit')
        online = True
        pass

    if online == True and isOnline() == False:
        status = 'Cellbit encerrou a live!'
        api.update_status(status)
        online = False
        checkStatus = False
        
        if len(gamesPlayed) > 0:
            date = dateStream()
            status = f"[{date['day']}/{date['month']}/{date['year']}] Games Jogados:\n\n"

            for game in gamesPlayed:
                addGame = f'• {game}\n'
                if len(addGame + status) < 280:
                    status += addGame
                elif len(addGame + status) > 280:
                    checkStatus = True
                    secondStatus += addGame

            if checkStatus == True:
                tweetId = api.user_timeline(screen_name='livesdocellbit')[0].id
                api.update_status(status, in_reply_to_status_id = tweetId)
                sleep(3)
                secondStatus += f'\nVOD: {getVideo()}'
                tweetId = api.user_timeline(screen_name='livesdocellbit')[0].id
                api.update_status(secondStatus, in_reply_to_status_id = tweetId)
            else:
                status += f'\nVOD: {getVideo()}'
                tweetId = api.user_timeline(screen_name='livesdocellbit')[0].id
                api.update_status(status, in_reply_to_status_id = tweetId)
        return
    
    global currentGame
    
    if isOnline():

        try:
            infos = getStream()
        except:
            return

        game = infos['game']
        timestampVod = f'{infos["vodHours"]}h{infos["vodMinutes"]}m{infos["vodSeconds"]}s'

        if game != currentGame:
            currentGame = game


            textPost = f'Cellbit está jogando: {game}\nMinutagem no VOD: ~{timestampVod} \nhttps://twitch.tv/cellbit'
            textTimestamp = f'Link do VOD: {getVideo()}?t={timestampVod}'

            try:
                getImageGame(game)
                sleep(2)
                if compareImages():
                    api.update_status(textPost)
                else:
                    api.update_status_with_media(textPost, 'gameImg.jpg')
            except:
                api.update_status(textPost)

            sleep(1)
            
            tweetId = api.user_timeline(screen_name='livesdocellbit')[0].id
            api.update_status(textTimestamp, in_reply_to_status_id = tweetId)
            
            gamesBlacklist = ['Just Chatting', 'Watch Party']
            if game in gamesBlacklist and game not in gamesPlayed:
                gamesPlayed.append(game)

bot.run("OTY4MTkzMzE0NTk3Nzc3NDc5.YmbSSg.IKhoiWVe7GWtFWncUGrBJ07304Q")