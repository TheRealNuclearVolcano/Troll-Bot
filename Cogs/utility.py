import discord
from discord.ext import commands

class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content[3:21] == str(self.client.user.id):
            await msg.channel.send("My prefix for this server is '>'")

    @commands.command()
    async def py(self, ctx, code):
        code_vars = {}
        try:
            exec(code, globals(), code_vars)
            result = ''
            for var in code_vars:
                result += f'{var} = {code_vars[var]}\n'
        except Exception as e:
            result = f'ERROR : {e}'
        await ctx.send(f'CODE :\n```{code} ``` \nRESULT :\n```{result} ```')


def setup(client):
    client.add_cog(Utility(client))
