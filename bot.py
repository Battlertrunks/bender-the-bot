import os
import discord
import requests
import time

from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GEOCODE_KEY = os.getenv('GEOCODE_API_KEY')
WEATHER_KEY = os.getenv('WEATHER_API_KEY')

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
        cur = time.localtime()

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

    # Creates the response
    response = (f'On this day in {year}, the {title} happened.\n'
                f'{desc}')

    # Sends the history of the day statement to Discord via bot
    await ctx.send(response)


@bot.command(name='weather')
async def weather(ctx):
    zipCode = ctx.message.content.split()[2]

    geoloc_url = 'https://trueway-geocoding.p.rapidapi.com/Geocode'
    geoloc_params = {'address': zipCode, 'language': 'en'}
    geoloc_headers = {
        'X-RapidAPI-Key': GEOCODE_KEY,
        'X-RapidAPI-Host': 'trueway-geocoding.p.rapidapi.com'
    }
    geoloc_r = requests.get(url = geoloc_url, params=geoloc_params, headers=geoloc_headers)
    geoloc_data = geoloc_r.json()
    resultAddress = geoloc_data['results'][0]
    longitude = resultAddress['location']['lng']
    latitude = resultAddress['location']['lat']
    
    weather_url = 'https://weatherapi-com.p.rapidapi.com/forecast.json'
    weather_params = {'q': f'{latitude},{longitude}'}
    weather_headers = {
        'X-RapidAPI-Key': WEATHER_KEY,
        'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
    }
    weather_r = requests.get(url=weather_url, params=weather_params, headers=weather_headers)
    weather_data = weather_r.json()

    city = resultAddress['locality']
    region = resultAddress['region']

    currentTemp = weather_data['current']['temp_f']
    condition = weather_data['current']['condition']['text']
    windSpeed = weather_data['current']['wind_mph']
    windDir = weather_data['current']['wind_dir']
    vis = weather_data['current']['vis_miles']
    
    response = (f'The weather at {city} {region}:\n'
    f'Current temperature is {currentTemp} fahrenheit\n'
    f'It is a {condition} day outside\n'
    f'Wind speed is {windSpeed} miles per hour in the direction {windDir}\n'
    f'Visibility is {vis} miles')

    await ctx.send(response)

bot.run(TOKEN)
