import discord
from discord.ext import commands
import praw
import random

reddit = praw.Reddit(client_id="secret", client_secret="secret", user_agent="classified lol")

class Fun(commands.Cog):
    """Funny commands lol"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme")
    async def meme(self, ctx):
        """again random crap now fight me irl"""
        submission = reddit.subreddit("memes").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @commands.command(name="sbubby")
    async def sbubby(self, ctx):
        """random crap nobody asked for lmao"""
        submission = reddit.subreddit("sbubby").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)
    
    @commands.command(name="crap")
    async def crapbrands(self, ctx):
        """also random crap nobody asked for lmao"""
        submission = reddit.subreddit("crappyoffbrands").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)
    
    @commands.command(name="subreddit", aliases=["sr"])
    @commands.is_nsfw()
    async def subreddit(self, ctx, subreddit):
        """This command is marked as NSFW until further notice. Apologies..."""
        submission = reddit.subreddit(f"{subreddit}").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
    print('Fun module loaded')
