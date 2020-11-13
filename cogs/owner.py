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
        self.token = 'token'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.api.set_auth("site", "token") # Set authorisation token for a bot list
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
