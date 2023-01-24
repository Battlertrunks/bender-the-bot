import os
import discord
import requests

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
bot = commands.Bot(command_prefix='!', intents=intents)

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

@bot.command(name='history')
async def hist(ctx):
    month = datetime.now().month
    day = datetime.now().day
    URL = f'https://byabbe.se/on-this-day/{month}/{day}/events.json'

    r = requests.get(url = URL)
    data = r.json()

    choosenEvent = data['events'][random.randrange(0, len(data['events']))]
    year = choosenEvent['year']
    title = choosenEvent['wikipedia'][0]['title']
    desc = choosenEvent['description']

    response = (f'On this day in {year}, the {title} happened.\n'
                f'{desc}')

    await ctx.send(response)

print(TOKEN)
bot.run(TOKEN)

