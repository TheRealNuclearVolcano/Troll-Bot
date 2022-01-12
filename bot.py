import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '>')

@client.event
async def on_ready():
    print('Logged in!')

@client.command()
async def ping(ctx):
    await ctx.send(f'The ping is {round(client.latency * 1000)}ms')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('your-bot-token')
