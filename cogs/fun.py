import discord
from discord.ext import commands
import praw

reddit = praw.Reddit()

class Fun(commands.Cog):
    """Funny commands lol"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        """again random crap now fight me irl"""
        submission = reddit.subreddit("memes").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def sbubby(self, ctx):
        """random crap nobody asked for lmao"""
        submission = reddit.subreddit("sbubby").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)
    
    @commands.command()
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
    
    @commands.command()
    async def cat(self, ctx):
        """Gives you a random cat."""
        submission = reddit.subreddit("cats").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        """Gives you a random dog."""
        submission = reddit.subreddit("dogpictures").random()
        embed = discord.Embed(title=f"{submission.title}")
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def taxcalc(self, ctx, amount: int):
        """Calculates tax on Dank Memer - a useful command for tax calclulations"""
        if amount < 20001:                    
            embed = discord.Embed(title="Dank Memer Tax Calculator", description=f"Amount entered: `{amount}`")
            embed.add_field(name=f"Amount expected to pay:", value=f"`{amount}`")
            embed.add_field(name=f"Amount lost by tax:", value=f"`0`")
            embed.add_field(name=f"Tax rate:", value="`0%`")
            await ctx.send(embed=embed)
        elif 20001 <= amount <= 50000:
            tax2 = amount * 1 / 100
            embed = discord.Embed(title="Dank Memer Tax Calculator", description=f"Amount entered: `{amount}`")
            embed.add_field(name=f"Amount expected to pay:", value=f"`{tax2 + amount}`")
            embed.add_field(name=f"Amount lost by tax:", value=f"`{tax2}`")
            embed.add_field(name=f"Tax rate:", value="`1%`")
            await ctx.send(embed=embed)
        elif 50001 <= amount <= 500000:
            tax3 = amount * 3 / 100
            embed = discord.Embed(title="Dank Memer Tax Calculator", description=f"Amount entered: `{amount}`")
            embed.add_field(name=f"Amount expected to pay:", value=f"`{tax3 + amount}`")
            embed.add_field(name=f"Amount lost by tax:", value=f"`{tax3}`")
            embed.add_field(name=f"Tax rate:", value="`3%`")
            await ctx.send(embed=embed)
        elif 500001 <= amount <= 1000000:
            tax4 = amount * 5 / 100
            embed = discord.Embed(title="Dank Memer Tax Calculator", description=f"Amount entered: `{amount}`")
            embed.add_field(name=f"Amount expected to pay:", value=f"`{tax4 + amount}`")
            embed.add_field(name=f"Amount lost by tax:", value=f"`{tax4}`")
            embed.add_field(name=f"Tax rate:", value="`5%`")
            await ctx.send(embed=embed)
        elif amount > 1000000:
            tax5 = amount * 8 / 100
            embed = discord.Embed(title="Dank Memer Tax Calculator", description=f"Amount entered: `{amount}`")
            embed.add_field(name=f"Amount expected to pay:", value=f"`{tax5 + amount}`")
            embed.add_field(name=f"Amount lost by tax:", value=f"`{tax5}`")
            embed.add_field(name=f"Tax rate:", value="`8%`")
            await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Fun(bot))
    print('Fun module loaded')
