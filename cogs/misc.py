import discord
from discord.ext import commands
import traceback
import sys
import os
import inspect

class Misc(commands.Cog):
    """Hmmm, what could these be for?"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinfo", aliases=['bi'])
    async def botinfo(self, ctx):
        """Shows info on the bot"""
        embed=discord.Embed(title="About Moderatus", description="Here is my info")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734822514894831639/fec64f576caff93fb238f64e7f282378.webp?size=128")
        embed.add_field(name="Prefix:", value="`m1/m!`", inline=True)
        embed.add_field(name="Developer:", value="`MrDragonBoi ඞ#7894`", inline=True)
        embed.add_field(name="Library:", value="`discord.py`", inline=True)
        embed.add_field(name="Servers:", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="Version:", value="`Alpha 1.7`", inline=True)
        embed.add_field(name="Support:", value=":star: [Here](https://discord.gg/EyKqRNT)", inline=True)
        embed.add_field(name="Invite:", value=":robot: [Invite](https://discord.com/oauth2/authorize?client_id=734822514894831639&permissions=2134240759&scope=bot)", inline=True)
        embed.add_field(name="Vote:", value=":white_check_mark: [Vote](https://discord.ly/moderatus/upvote)", inline=True)
        embed.add_field(name="Donate:", value=":pound: [Donate](https://www.patreon.com/join/moderatus)", inline=True)
        embed.add_field(name="Python Version", value=f"`{sys.version}`", inline=True)
        embed.add_field(name="discord.py Version", value=f"`{discord.__version__}`", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Shows the bot's ping"""
        embed=discord.Embed(title="PONG!", description=f'My latency is at least 69% likely to be: **{round(ctx.bot.latency * 1000)}ms**')
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=['si'])
    async def serverinfo(self, ctx): 
        """Shows info on the server"""
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
        """(Required under Discord ToS)"""
        embed=discord.Embed(title="Moderatus' Privacy Policy", description="Correct at 25/09/2020 British Summer Time")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/744111535638446121/744112274364432454/Privacy.png')
        embed.add_field(name="**What data do we collect?**", value="We do not collect nor share any data, except for the serverinfo and/or other commands.", inline=False)
        embed.add_field(name="**What happens if I have a problem?**", value="If you have questions regarding your privacy, this privacy policy or this bot in general you may contact me using one of the forms of contact listed below;", inline=False) 
        embed.add_field(name="• Email -", value="`realuprising2005@gmail.com`", inline=False)
        embed.add_field(name="• Discord -", value="`MrDragonBoi ඞ#7894 (541872670371741697)`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="support", aliases=['sup', 'server'])
    async def support(self, ctx):
        """Support server invite"""
        await ctx.send("https://discord.gg/EyKqRNT")

    @commands.command(name="bugreport")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bug(self, ctx, message):
        """Report bugs directly to the owner!"""
        channel = self.bot.get_channel(762306208580370464)
        embed = discord.Embed(title='Bug report!', description='Your bug report, along with your discord name, discriminator, and id were sent to the bot owner. He will look into your report and hopefully fix the issue soon!', colour=discord.Color.green())
        if channel is None:
            await ctx.send('Unable to send request.')
        else:
            await channel.send(f'{ctx.message.content} | User: {ctx.message.author} ID: {ctx.message.author.id}')
            await ctx.send(embed=embed)

    @commands.command(name="suggest")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def suggest(self, ctx, message):
        """Suggest features directly to the owner! Make sure you have DMs on and join the server!"""
        channel = self.bot.get_channel(762306208580370464)
        embed = discord.Embed(title='Suggestion!', description='Your suggestion, along with your discord name, discriminator, and id were sent to the bot owner. He will look into your report and hopefully add the feature soon!', colour=discord.Color.green())
        if channel is None:
            await ctx.send('Unable to send request.')
        else:
            await channel.send(f'{ctx.message.content} | User: {ctx.message.author} ID: {ctx.message.author.id}')
            await ctx.send(embed=embed)

    @commands.command(name="news")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def news(self, ctx):
        """Announcements regarding Moderatus. Make sure to join the server as well!"""
        embed = discord.Embed(title='What\'s New?', description='Here is the new stuff added/removed!')
        embed.add_field(name="Current version:", value="Alpha 1.7")
        embed.add_field(name="Added", value="Prefix command (about time!) + source command (links to GitHub)")
        embed.add_field(name="Removed", value="N/A")
        embed.add_field(name="Other", value="This do be quick tho")
        embed.add_field(name="Fixed", value="N/A")
        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx, *, command: str = None):
        """Displays my full source code or for a specific command."""
        source_url = 'https://github.com/moderatus-inc/moderatus'
        branch = 'master'
        if command is None:
            return await ctx.send(source_url)
        elif command == 'developer':
            await ctx.send('That isn\'t really a command, is it?')
        elif command == 'help':
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace('.', ' '))
            if obj is None:
                return await ctx.send('Could not find command.')

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith('discord'):
            # not a built-in command
            location = os.path.relpath(filename).replace('\\', '/')
        else:
            location = module.replace('.', '/') + '.py'
            source_url = 'https://github.com/moderatus-inc/moderatus'
            branch = 'master'

        final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
        await ctx.send(final_url)

def setup(bot):
    bot.add_cog(Misc(bot))
    print('Misc module loaded.')
