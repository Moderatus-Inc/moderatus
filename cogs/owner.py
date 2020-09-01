from discord.ext import commands
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import aiohttp
import discordlists


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = discordlists.Client(self.bot)  # Create a Client instance
        self.api.set_auth("discordbotlist.com", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxLCJpZCI6IjczNDgyMjUxNDg5NDgzMTYzOSIsImlhdCI6MTU5ODYwMjY1NH0.fHfVHx9HM6Rh9u3C1R2U3HBjVdwQO7Qb0FTDeFfsHqw") # Set authorisation token for a bot list
        self.api.set_auth("discord.boats", "e0U24Er1CkNgJGr0sHxhtwaFmdVQhj8S19PBVO0VDBNVEerrSMrswmHWloqybrCE7HaqSES4lF2xOzSuKDjepj8V78tRoBcl99pgCzH5XC2NhLoOc40DGoj7zizTS8QsM4Dc5CmTIuyJ1N7s2y9o0BJDuJy")
        self.api.set_auth("botlist.space", "21e50a2dc17108531e8f0471afca5e0bd121656a860a994029905d982859ee74f85dd160ac76d9a4d0a0e831235b1a90")
        self.api.set_auth("discordextremelist.xyz", "DELAPI_23c265e915080ebaf6bf4317df281bf4-734822514894831639")
        self.api.set_auth("glennbotlist.xyz", "GBL_5a6c7dfee5d243b98be3aa43a83facb0b4e3e39877cc43d59a208873b78f26af6d5a3c9dab8d438ca339e4ce86b32820")
        self.api.set_auth("disforge.com", "df36c16767a13fadebc5b0a60bd3cfdbf385d307777ef4685ef0bd046642e8b5")
        self.api.set_auth("discordlabs.org", "discordlabs.org-WUJGI1CAJFed4GPHQqwr")
        self.api.set_auth("discord.bots.gg", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOnRydWUsImlkIjoiNTQxODcyNjcwMzcxNzQxNjk3IiwiaWF0IjoxNTk4ODk3NDg4fQ.aj8LgxfH_haWSJIFMuEU_avjgKZlhMX8dgtFc-lZJ2A")
        self.api.start_loop()  # Posts the server count automatically every 30 minutes

    @commands.command(name="post")
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

    @commands.command(name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body):
        """Evaluates python code"""
        env = {
            'ctx': ctx,
            'bot': self.bot,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
            return content.strip('` \n')

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))
        
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        
                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')  # tick
        elif err:
            await ctx.message.add_reaction('\u2049')  # x
        else:
            await ctx.message.add_reaction('\u2705')

def setup(bot):
    bot.add_cog(Owner(bot))
    print('Owner module loaded')