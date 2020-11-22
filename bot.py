import discord
from discord.ext import commands
import asyncio
from pretty_help import PrettyHelp
import json
from pathlib import Path
from discord import Colour
import sys

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

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
    bot.loop.create_task(servers())

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
    
    prefixes.pop(str(guild.id))

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
        embed = discord.Embed(title="Frick!", description="You tried to use developer commands, but guess what? You're not MrDragonBoi ඞ#7894! Also, don't even think about hacking his account, you idot")
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Frick!", description="You never specified the right arguments. Like, go get a life, n00b!")
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Frick!", description="This command is on cooldown. Probably since you're going too fast lol n00b")
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Frick!", description="I don't have the perms for this command, maybe see about giving me the right perms?")
        await ctx.send()
    if isinstance(error, commands.NSFWChannelRequired):
        embed = discord.Embed(title="Frick!", description="This command is ONLY available in NSFW channels. Nice try, n00b!")
        await ctx.send(embed=embed)

def read_json(filename):
    with open(f"{cwd}/{filename}.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"{cwd}/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)

bot.load_extension("cogs.moderation")    
bot.load_extension("cogs.misc")
bot.load_extension("cogs.music")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.fun")
bot.load_extension("jishaku")
bot.run('TOKEN', bot=True)
