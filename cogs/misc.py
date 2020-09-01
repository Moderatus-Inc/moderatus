import discord
from discord.ext import commands
from datetime import datetime
import traceback
import sys

class Misc(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    @commands.command(name="botinfo", aliases=['bi'])
    async def botinfo(self, ctx):
        """
        Shows info on the bot
        """
        embed=discord.Embed(title="About Moderatus", description="Here is my info")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734822514894831639/bde485834ec5b3351356f045b4dc9655.png?size=128")
        embed.add_field(name="Prefix:", value="`m1/m!`", inline=True)
        embed.add_field(name="Developer:", value="`MrCatLover#7894`", inline=True)
        embed.add_field(name="Library:", value="`discord.py`", inline=True)
        embed.add_field(name="Servers:", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="Version:", value="`v1.0.5`", inline=True)
        embed.add_field(name="Users:", value=f"`{len(self.bot.users)}`", inline=True)
        embed.add_field(name="Support:", value=":star: [Here](https://discord.gg/EyKqRNT)", inline=True)
        embed.add_field(name="Invite:", value=":robot: [Invite](https://discord.com/oauth2/authorize?client_id=734822514894831639&permissions=2134240759&scope=bot)", inline=True) 
        embed.add_field(name="Vote:", value=":white_check_mark: [Vote](https://discord.ly/moderatus/upvote)", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)
    
    @commands.command(name="avatar", aliases=['pfp, av, profilepic'])
    async def avatar(self, ctx, User: discord.Member):
        """
        Shows the user's profile pic
        """
        embed=discord.Embed(title="User's Profile pic", description="Here is the user's profile pic you requested...")
        embed.set_thumbnail(url=f"{User.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Shows the bot's ping
        """
        embed=discord.Embed(title="Pong!", description=f'{ctx.bot.latency * 100}ms')
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=['si'])
    async def serverinfo(self, ctx): 
        """
        Shows info on the server
        """
        embed=discord.Embed(title=f"About {ctx.guild.name}", description=f"Here is {ctx.guild.name}('s) info")
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name="Boosts:", value=f"`{ctx.guild.premium_subscription_count}`", inline=True)
        embed.add_field(name="Owner:", value=f"`{ctx.guild.owner}`", inline=True)            
        embed.add_field(name="Boost tier:", value=f"`{ctx.guild.premium_tier}`", inline=True)
        embed.add_field(name="Users:", value=f"`{len(ctx.guild.members)}`", inline=True)
        embed.add_field(name="Channels:", value=f"`{len(ctx.guild.channels)}`", inline=True)
        embed.add_field(name="Roles:", value=f"`{len(ctx.guild.roles)}`", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command(name="privacy")
    async def privacy(self, ctx):
        """
        (Required under Discord ToS)
        """
        embed=discord.Embed(title="Moderatus' Privacy Policy", description="Correct at 15/08/2020 British Summer Time")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/744111535638446121/744112274364432454/Privacy.png')
        embed.add_field(name="**What data do we collect?**", value="We do not collect nor share any data, except for the serverinfo and/or other commands.", inline=False)
        embed.add_field(name="**What happens if I have a problem?**", value="If you have questions regarding your privacy, this privacy policy or this bot in general you may contact me using one of the forms of contact listed below;", inline=False) 
        embed.add_field(name="• Email -", value="`realuprising2005@gmail.com`", inline=False)
        embed.add_field(name="• Discord -", value="`MrCatLover#7894 (541872670371741697)`", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="vote", aliases=['upvote'])
    async def vote(self, ctx):
        """
        Vote for Moderatus
        """
        embed=discord.Embed(title="Vote for moderatus!", description="Here are the current vote links.")
        embed.add_field(name="Vote every 12 hours", value="[Discord Labs](https://bots.discordlabs.org/bot/734822514894831639), [DiscordBoats](https://discord.boats/bot/734822514894831639/vote)", inline=False)
        embed.add_field(name="Vote every 24 hours", value="[DBL](https://discord.ly/moderatus/upvote), [BotlistSpace](https://botlist.space/bot/734822514894831639/upvote)", inline=False)
        embed.add_field(name="Vote at any time", value="[BBL](https://bladebotlist.xyz/bot/734822514894831639)", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="invite", aliases=['inv'])
    async def invite(self, ctx):
        """
        Invite Moderatus to your server
        """
        embed=discord.Embed(title="Invite Moderatus!", description="Doitdoitdoitdoitdoitdoit")
        embed.add_field(name="Here:", value="[Doitdoitdoitdoitdoitdoit](https://discord.com/oauth2/authorize?client_id=734822514894831639&permissions=2134240759&scope=bot)", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="support", aliases=['sup', 'server'])
    async def support(self, ctx):
        """
        Support server invite
        """
        await ctx.send("https://discord.gg/EyKqRNT")

def setup(bot):
    bot.add_cog(Misc(bot))
    print('Misc module loaded.')