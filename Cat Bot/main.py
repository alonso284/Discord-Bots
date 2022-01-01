import discord
import requests
import json
import os

#from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('cat'):
        url = 'https://api.thecatapi.com/v1/images/search?'
        headers = {'x-api-key': os.getenv("catAPIkey")}
        r = requests.get(url, headers=headers)
        catImg = json.loads(r.text)[0]["url"]

        embed = discord.Embed(
            title="Here, have a cat", color=discord.Colour.purple())
        embed.set_image(url=catImg)

        await message.channel.send(embed=embed)

    if message.content.startswith('dog'):
        url = 'https://api.thedogapi.com/v1/images/search?'
        headers = {'x-api-key': os.getenv("dogAPIkey")}
        r = requests.get(url, headers=headers)
        catImg = json.loads(r.text)[0]["url"]

        embed = discord.Embed(
            title="Here, have a dog", color=discord.Colour.purple())
        embed.set_image(url=catImg)

        await message.channel.send(embed=embed)


token = os.getenv("token")
client.run(token)
