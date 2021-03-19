import discord
import requests
import os
from discord.ext import commands

from dotenv import load_dotenv
from pathlib import Path 
 
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")
client = commands.Bot(command_prefix='!')

# default discord colors, we can get something better 
Colors = { 
    'default' : discord.Color.default(),
    'teal' : discord.Color.teal(),
    'turtle' : discord.Color.dark_teal(),                 
    'green' : discord.Color.green(),
    'evergreen' : discord.Color.dark_green(),
    'blue' : discord.Color.blue(),
    'purple' : discord.Color.purple(),
    'violet' : discord.Color.dark_purple(),
    'magenta' : discord.Color.magenta(),
    'pink' : discord.Color.dark_magenta(),
    'gold' : discord.Color.gold(),
    'sun' : discord.Color.dark_gold(),
    'orange' : discord.Color.orange(),
    'tangerine' : discord.Color.dark_orange(),
    'red' : discord.Color.red(),
    'blood' : discord.Color.dark_red() 
}

#we need to add a role everytime a user joins the server to edit attributes
#ex. color

@client.event
async def on_member_join(member):
    await client.add_roles(member, member.name)

@client.command(name="color", help="change your name to a different color")
async def color(ctx, args):
    r = discord.utils.get(ctx.guild.roles, name=ctx.message.author.name)
    if args in Colors.keys():
        await r.edit(server=ctx.message.guild, role=r, color=Colors[args])
    else:
        await ctx.send("testing 4,5")

#uses an api to generate a meme
@client.command(name='generate-meme', help='enter the image, top text, and bottom text with a / in between each ')
async def generate_meme(ctx, args):
  
    image = ""
    top = ""
    bottom =""
    print(args)
    count = 0
    
    #loop through args to get meme phrases and using / as the delimiter
    #hacky but open to better solutions
    for i in args:
        if(i == '/'):
            count += 1
            continue
        
        if count == 0:
            image += i
        if count == 1: 
            top += i
        if count == 2:
            bottom += i
    
    url = "https://ronreiter-meme-generator.p.rapidapi.com/meme"
    querystring = {"meme":image.strip(),"bottom":bottom.strip(),"top":top.strip(),"font_size":"50","font":"Impact"}

    headers = {
        'x-rapidapi-key': os.getenv("RAPID_API_SECRET"),
        'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    #read into a file then display the image
    #a little hacky open to better solutions
    
    file = open("sample_image.png", "wb")
    file.write(response.content)
    file.close()
    
    await ctx.send(file=discord.File('sample_image.png'))
   
            
@client.command(name='list-meme-images', help='25 images you can use for your meme, see full list at apimeme.com')
async def get_images(ctx):
    images = []
    url = "https://ronreiter-meme-generator.p.rapidapi.com/images"

    headers = {
        'x-rapidapi-key': os.getenv("RAPID_API_SECRET"),
        'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        count = 0
        for i in response.json():
            if(count == 25): 
                break
            images.append(i)
            count += 1
        
        await ctx.send(images)
    else:
        await ctx.send("could not connect to api")

#straight forward function generate a random meme from an api
@client.command(name='quote', help='generate a random quote from Zen API')
async def get_quote(ctx): 
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        for i in response.json():
            print(i)
        await ctx.send('{} -{}'.format(i['q'], i['a']))
    else:
        await ctx.send("could not connect to external API") 

#creates a new channel on the discord
@client.command(name='create-channel', help="type create-channel with a one world name after it to create a new channel")
async def create_channel(ctx, arg):
    guild = ctx.guild
    channel = discord.utils.get(guild.channels, name=arg)
    if not channel:
        await guild.create_text_channel(arg)

#displays a picture of the matrix screensaver
@client.command(name='matrix', help="follow the white rabbit")
async def print_matrix(ctx):
    print("this ran at least")
    await ctx.send("https://source.unsplash.com/iar-afB0QQw")

client.run(TOKEN)

