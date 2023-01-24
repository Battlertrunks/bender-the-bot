import os
import discord
import requests
import time
import random
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!Bender ', intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    someSentence = 'Hello Human!'

    if message.content == '99!':
        response = someSentence
        await message.channel.send(response)

historyListNumber = 0
cur = time.localtime()

@bot.command(name='history')
async def hist(ctx):
    # Getting todays date and number of times this command was used
    global historyListNumber, cur
    month = datetime.now().month
    day = datetime.now().day

    # Making the request and gathering the data
    URL = f'https://byabbe.se/on-this-day/{month}/{day}/events.json'

    r = requests.get(url = URL)
    data = r.json()

    # Checks if it is a new day, if so resets the historyListNumber to 0
    if cur[:3] != time.localtime()[:3]:
        historyListNumber = 0

    # If there is no more history events 
    if len(data['events']) < historyListNumber:
        await ctx.send('Sorry, no more history of the day :(')
        return

    # Breaks the object up to use in a statement
    # choosenEvent = data['events'][random.randrange(0, len(data['events']))]
    choosenEvent = data['events'][historyListNumber]
    year = choosenEvent['year']
    title = choosenEvent['wikipedia'][0]['title']
    desc = choosenEvent['description']
    historyListNumber +=1
    print(historyListNumber)

    # Creates the response
    response = (f'On this day in {year}, the {title} happened.\n'
                f'{desc}')

    # Sends the history of the day statement to Discord via bot
    await ctx.send(response)

bot.run(TOKEN)
