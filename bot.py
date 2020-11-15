import discord
from discord.ext import commands
import asyncio
from pretty_help import PrettyHelp
import json

def prefix(bot, message):
    with open("prefixes.json") as f:
        prefixes = json.load(f)
        default = ["m!", "m1"]

    return commands.when_mentioned_or(*prefixes, *default)(bot, message)

intents = discord.Intents.default()

bot = commands.AutoShardedBot(
    command_prefix=prefix,
    intents=intents,
    description='A discord.py Moderation + Music bot made by MrDragonBoi ඞ#7894 since July 2020.',
    owner_id=541872670371741697,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False),
    help_command=PrettyHelp()
)

bot.snipes = {}

@bot.event
async def on_message_delete(message):
    bot.snipes[message.channel.id] = message

async def servers():
    while True:

        servers = f"{len(bot.guilds)} server(s) | m!help or m1help | moderatus.xyz"
        
        await bot.change_presence(activity=discord.Game(name=servers))
        
        await asyncio.sleep(10)

        await bot.change_presence(activity=discord.Game(name=servers))

@bot.command(name="snipe", pass_context=True)
async def snipe(ctx, *, channel: discord.TextChannel = None):
    """👀"""
    channel = channel or ctx.channel
    try:
        msg = bot.snipes[channel.id]
    except KeyError:
        return await ctx.send('Nothing to snipe!')
    # one liner, dont complain
    await ctx.send(embed=discord.Embed(description=msg.content, color=msg.author.color).set_author(name=str(msg.author), icon_url=str(msg.author.avatar_url)))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(bot.guilds)} server(s) | m!help or m1help | moderatus.xyz'))
    bot.load_extension("cogs.moderation")
    bot.load_extension("cogs.misc")
    bot.load_extension("cogs.music")
    bot.load_extension("cogs.owner")
    bot.load_extension("cogs.fun")
    bot.loop.create_task(servers())
    return

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = ['m1', "m!"]

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes.pop[str(guild.id)]

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.command(name="prefix", pass_context=True)
@commands.guild_only()
@commands.has_guild_permissions(administrator=True, manage_guild=True)
async def _prefix(ctx, prefix):
    """Changes the server's prefix"""
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send(f'Nice try! You can\'t use owner commands if you\'re not MrDragonBoi ඞ#7894. He is the only one with the perms.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'You didn\'t specify the right arguments for this command.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f'I don\'t have the perms to perform this action.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'You don\'t have the perms to perform this action.')
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(f'This command does not work in non-NSFW channels. Apologies')

bot.run('Super duper secret token no looky 👀', bot=True)
