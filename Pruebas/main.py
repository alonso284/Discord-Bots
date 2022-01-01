from itertools import cycle
import random
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
load_dotenv()

client = commands.Bot(command_prefix='+')
status = cycle(['Status 1', 'Status2'])


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello World!'))
    print('We have logged in as {0.user}'.format(client))
    change_status.start()

# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please pass in all required')
#     elif isinstance(error, commands.CommandNotFound):
#         await ctx.send('Command not found')


# @client.command()
# async def ping(ctx):
#     await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# any of these will run the same command
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['suck it', 'ily', 'idk bruh']
    await ctx.send(f'question: {question}\n Answer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{ctx.author.display_name} deleted {amount} messages')


@client.command()
@commands.has_permissions(manage_messages=True)
async def errase(ctx, amount: int):
    await ctx.channel.purge(limit=None)
    await ctx.send(f'{ctx.author.display_name} deleted {amount} messages')


@errase.error
async def errase_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('errase needs a second argument')


def is_it_me(ctx):
    return ctx.author.id == 314871835227455499


@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'Hi I\'m {ctx.author.mention}')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{ctx.author.mention} kicked {member.mention}')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{ctx.author.mention} banned {member.mention}')


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    print('starting unban')

    for ban_entry in banned_users:

        user = ban_entry.user
        print('looking for ' + user.name)
        print(user.name)
        print(user.discriminator)
        print(member_name)
        print(member_discriminator)

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.purge(limit=1)
            await ctx.send(f'{ctx.author.mention} unbanned {user.mention}')
            return


@tasks.loop(seconds=6)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send(message.author.name)

@client.event
async def on_member_join(member):
    print(f'{member}has joined the server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

client.run(os.getenv('PruebasToken'))
