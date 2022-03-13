import random
import praw
import discord
from discord.ext import commands

reddit = praw.Reddit(
    client_id = 'client_id',
    client_secret = 'client_secret',
    user_agent = 'user_agent',
    username = 'username')

def memes():
    posts = []
    sub = reddit.subreddit('meme')
    top = sub.hot(limit=200)
    for post in top:
        posts.append(post)
    print('Memes loaded')
    return posts

class Meme(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.posts = memes()

    @commands.command()
    async def meme(self, ctx):
        post = random.choice(self.posts)
        self.posts.remove(post)
        embed = discord.Embed(title=post.title, url=f"https://www.reddit.com{post.permalink}")
        embed.set_image(url=post.url)
        await ctx.send(embed=embed)
        if len(self.posts) < 50:
            self.posts = await memes()


def setup(client):
    client.add_cog(Meme(client))
