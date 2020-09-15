import discord
import asyncio
from discord.ext import commands
from pretty_help import PrettyHelp

def get_prefix(client, message):

    prefixes = ['m!', 'm1']

    if not message.guild:
        prefixes = ['m!']

    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(                         
    command_prefix=get_prefix,              
    help_command=PrettyHelp(color=discord.Color.dark_red()),
    description='A bot used for moderation. I can do ban and kick punishments. I cannot, however unban right now.',
    owner_id=541872670371741697,            
    case_insensitive=False,
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False)
)

@bot.event
async def on_ready():                                       
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(bot.users)} user(s) in {len(bot.guilds)}/100 server(s) | m!help or m1help'))
    bot.load_extension("cogs.moderation")
    bot.load_extension("cogs.misc")
    bot.load_extension("cogs.music")
    bot.load_extension("cogs.owner")
    return
    
bot.run('TOKEN', bot=True, reconnect=True)
