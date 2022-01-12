import random, json
import discord
from discord.ext import commands

data_f = open('data.json')
data = json.load(data_f)

insults = data['insults']

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def insult(self, ctx, user=None):
        if user == None:
            user = ctx.author.mention
        if (user.replace(' ', ''))[3:-1] == str(self.client.user.id):
            await ctx.send("No")
            return
        await ctx.send(f'{user} {random.choice(insults)}')

    @commands.command()
    async def uwu(self, ctx):
        await ctx.send('UwU')

    @commands.command()
    async def owo(self, ctx):
        await ctx.send('OwO')

    @commands.command()
    async def twt(self, ctx):
        await ctx.send('TwT')

    @commands.command()
    async def lenny(self, ctx):
        await ctx.send('( ͡° ͜ʖ ͡°)')

    @commands.command()
    async def troll(self, ctx):
        await ctx.send(file=discord.File('bot_data/img/troll.gif'))

    @commands.command()
    async def trollsad(self, ctx):
        await ctx.send(file=discord.File('bot_data/img/troll_sad.gif'))


def setup(client):
    client.add_cog(Fun(client))
