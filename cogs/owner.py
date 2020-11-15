from discord.ext import commands, tasks
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import aiohttp
import discordlists
import discord
import logging
import sys
import dbl

class Owner(commands.Cog):
    """Super secret commands no touchy""" 
    
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.api = discordlists.Client(self.bot)  # Create a Client instance
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczNDgyMjUxNDg5NDgzMTYzOSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjAzODE3MTA1fQ.awpY05Dv1UXh5bIqPq2cs6KnwWZjno2K-UziVC0HVWI'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.api.set_auth("discordbotlist.com", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxLCJpZCI6IjczNDgyMjUxNDg5NDgzMTYzOSIsImlhdCI6MTYwMzg3ODY4NH0.6wVaD15AzFMHXhhRDVIeX8X56mxWr8I-ReSDOaoqnSw") # Set authorisation token for a bot list
        self.api.set_auth("discord.boats", "e0U24Er1CkNgJGr0sHxhtwaFmdVQhj8S19PBVO0VDBNVEerrSMrswmHWloqybrCE7HaqSES4lF2xOzSuKDjepj8V78tRoBcl99pgCzH5XC2NhLoOc40DGoj7zizTS8QsM4Dc5CmTIuyJ1N7s2y9o0BJDuJy")
        self.api.set_auth("botlist.space", "21e50a2dc17108531e8f0471afca5e0bd121656a860a994029905d982859ee74f85dd160ac76d9a4d0a0e831235b1a90")
        self.api.set_auth("discordextremelist.xyz", "DELAPI_23c265e915080ebaf6bf4317df281bf4-734822514894831639")
        self.api.set_auth("disforge.com", "df36c16767a13fadebc5b0a60bd3cfdbf385d307777ef4685ef0bd046642e8b5")
        self.api.set_auth("discordlabs.org", "discordlabs.org-x5Jnim3V5msOy5bMMQq0")
        self.api.set_auth("discord.bots.gg", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOnRydWUsImlkIjoiNTQxODcyNjcwMzcxNzQxNjk3IiwiaWF0IjoxNTk4ODk3NDg4fQ.aj8LgxfH_haWSJIFMuEU_avjgKZlhMX8dgtFc-lZJ2A")
        self.api.set_auth("discordlistology.com", "41bdd206a569e31dd36a51fe8952afe3b5c9b2bc76bcf473da968cc58e7ff16401260244fdd89f057034e9b62e3db5c6c84f616cf3f568bef58417ccbfa895db45cc67e54714d68e59ebbec8fbc007f3602ab1a7823225f081685dcddbae0e33197e9bdec7a0821e25b1b1ecce37bd1af4822d9b714841f1ddf91fe3fdd2effb7b7bacdc8a38bf7c89e807b69bb82b9151c11f61aa665d03c705edb8594b5f0f1af17a263763b7920f21ef867638299ad0c5d1eba1a188e1df9bcb596ccf96588cf124d59a79f9cf5974dc4c7e3cbcf4fb880cbf66493fab2889ac501b1fe6fd2e8d09bd0a92932a7f95c99fa70496eb073c9cf54e1a8b843fbeca17eaade7a127169347a862a4320074bd9a69ac0823f90475462f2c5ae25c746af43bd2563780d416422d505a9dc819eac78089c810562ac8f555e4b67b58f08c17cc78d91f92fd71f02927d8080d42a3c53e10d34b6f50da27f5d8109f4fc7c2f18cb6d72460273771871b77112f059d72e3f8d251f40b3416c9771ad791a5a194d06791ca451510c39f39bf0ecf7c546999f065d54234801bdf02c6518b7ff6a27f74b95d0bf7b94299edcc19da27d9d736a24550f566f9195370768619860ccb697402205c0bda3f2c09e747")
        self.api.set_auth("topcord.xyz", "oXwCPF8zBvy2AYSNpXbOHA7OYz5dZ18w")
        self.api.set_auth("mythicalbots.xyz", ".JvzQrAf.twyj-OnPJnAS6A2TXCOvxG6l7oDw4yVrJeY5M0B6l")
        self.api.set_auth("botsfordiscord.com", "05152acbf48eebdec2500051972043f1713d1d1d15bad48c2a1085b0ee0596ca3c1fb400b85730bd9187b31572636413fc81688bcb55a8b56c49650bc6e20f94")
        self.api.set_auth("voidbots.net", "ZpcZcUNO4uWnwHWlWJIb")
        self.api.set_auth("bladebotlist.xyz", "41XBEnZWRnleq9idNcJl")
        self.api.set_auth('distop.xyz', 'zsv84humy4qx1kz9xgm6')
        self.api.start_loop()  # Posts the server count automatically every 30 minutes

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')
    
    @commands.is_owner()
    @commands.group(pass_context=True)
    async def developer(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You didn\'t provide a command.') 

    @commands.is_owner()
    @developer.command(name='connectshard', hidden=True, alias="cs")
    async def connectshard(self, ctx, shard: discord.ShardInfo):
        await shard.connect(shard)

    @commands.is_owner()
    @developer.command(name='disconnectshard', hidden=True, alias="ds")
    async def disconnectshard(self, ctx, shard: discord.ShardInfo):
        await shard.disconnect(shard)
    
    @commands.is_owner()
    @developer.command(name='reconnectshard', hidden=True, alias="rs")
    async def reconnectshard(self, ctx, shard: discord.ShardInfo):
        await shard.reconnect(shard)

    @developer.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @developer.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @developer.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @developer.command(name="post")
    @commands.is_owner()
    async def post(self, ctx: commands.Context):
        """
        Manually posts guild count using discordlists.py (BotBlock)
        """
        try:
            result = await self.api.post_count()
        except Exception as e:
            await ctx.send("Request failed: `{}`".format(e))
            return

        await ctx.send("Successfully manually posted server count ({:,}) to {:,} lists."
                       "\nFailed to post server count to {:,} lists.".format(self.api.server_count,
                                                                             len(result["success"].keys()),
                                                                             len(result["failure"].keys())))

    @developer.command(name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body):
        """Evaluates python code"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @developer.command()
    async def check_cogs(self, ctx, cog_name):
        try:
            self.bot.load_extension(f"cogs.{cog_name}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send("Cog is loaded")
        except commands.ExtensionNotFound:
            await ctx.send("Cog not found")
        else:
            await ctx.send("Cog is unloaded")
            self.bot.unload_extension(f"cogs.{cog_name}")
    
    @developer.command(name="reloadall", aliases=["ra"])
    async def _reload_all(self, ctx):
        """Reloads all modules"""
        if commands.ExtensionAlreadyLoaded:
            await ctx.send('All cogs loaded. Reloading...')
            self.bot.reload_extension('cogs.owner')
            self.bot.reload_extension('cogs.misc')
            self.bot.reload_extension('cogs.music')
            self.bot.reload_extension('cogs.moderation')
        else:
            await ctx.send('All cogs are now locked \'n\' loaded mate.')

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        logger.info('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(Owner(bot))
    print('Owner module loaded')
