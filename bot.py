from functions.twitchAPI import verifyGame, isOnline, getImageGame, getTitle, returnTimestamp

import os
from time import sleep

import discord
from discord.ext import tasks

import tweepy

global currentGame, online

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
    currentGame = verifyGame()

@bot.event
async def on_ready():
    print('Online!')
    checkGame.start()

@tasks.loop(seconds=15)
async def checkGame():
    if isOnline() == True and online == False:
        api.update_status(f'Cellbit entrou ao vivo!\nTítulo: {getTitle}\nhttps://twitch.tv/cellbit')
    if online == True and isOnline() == False:
        api.update_status('Cellbit encerrou a live!')
    global currentGame
    if isOnline():
        game = verifyGame()
        if game != currentGame:
            currentGame = game
            textPost = f'Cellbit está jogando: {game}\nhttps://twitch.tv/cellbit'
            # getImageGame(game)
            sleep(3)
            # api.update_status_with_media(textPost, 'gameImg.jpg')

bot.run("OTY4MTkzMzE0NTk3Nzc3NDc5.YmbSSg.IKhoiWVe7GWtFWncUGrBJ07304Q")
