import discord
from discord.ext import commands
import sys
import traceback
from typing import Optional

class Moderation(commands.Cog):    
    """Kick rule breaker butt with these commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, reason: Optional[str]):
        """Bans a user"""
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't ban a higher up role.")
            await ctx.send(embed=embed)
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't ban a same rank.")
            await ctx.send(embed=embed) 
        elif member == ctx.author:
            embed = discord.Embed(title=":x: You cannot ban yourself! If you are feeling/having suicidal/self-harm thoughts, visit https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines")
            await ctx.send(embed=embed)
        elif member == member.id(734822514894831639):
            embed = discord.Embed(title=":x: w-why do you want to ban me? What the heck did I do? :(")
            await ctx.send(embed=embed)
        else:   
            await member.ban(reason=reason)
            embed = discord.Embed(title=f":white_check_mark: {member} was banned; {reason}.")
            await ctx.send(embed=embed)
            
            try:
                channel = await member.create_dm()
                await channel.send(f'You were banned in {ctx.guild.name} for {reason}.')
            except discord.HTTPException:
                embed = discord.Embed(title=f":white_check_mark: {member} was banned; {reason}. I have recieved an error, so I cannot DM the user.")
                await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unban(self, ctx, member: discord.Member, reason: Optional[str]):
        """Unbans a user"""
        if member == None:
            embed = discord.Embed(title=":x: You need to sepcify a user!")
            await ctx.send(embed=embed)
        else:
            await member.unban(reason=reason)
            embed = discord.Embed(title=f":white_check_mark: {member} was unbanned; {reason}")
            await ctx.send(embed=embed) 

    @commands.guild_only()
    @commands.command(name="mute")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member, reason: Optional[str]):
        """Mutes a user"""
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't mute a higher up role.")
            await ctx.send(embed=embed)
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't mute a same rank.")
            await ctx.send(embed=embed) 
        elif member == ctx.author:
            embed = discord.Embed(title=":x: You cannot mute yourself! If you are feeling/having suicidal/self-harm thoughts, visit https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines")
            await ctx.send(embed=embed)       
        elif not discord.utils.get(name="Muted", permissions=discord.Permissions(send_messages=True, manage_messages=False)):
            await ctx.create_role(name="Muted", permissions=discord.Permissions(send_messages=True, manage_messages=False))
        else:
            await ctx.add_roles(name="Muted", reason=reason)
            try:
                channel = await member.create_dm()
                await channel.send(f'You were muted in {ctx.guild.name} for {reason}.')
            except discord.HTTPException:
                embed = discord.Embed(title=f":white_check_mark: {member} was muted; {reason}. I have recieved an error, so I cannot DM the user.")
                await ctx.send(embed=embed)
            
    @commands.guild_only()
    @commands.command(name="unmute")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, reason: Optional[str]):
        """Unmutes a user"""   
        await discord.utils.get(name="Muted", permissions=discord.Permissions(send_messages=True, manage_messages=False))
        await ctx.remove_roles(name="Muted", reason=reason)
        channel = await member.create_dm()
        await channel.send(f'You were unmuted in {ctx.guild.name} for {reason}.')
        embed = discord.Embed(title=f":white_check_mark: {member} was unmuted; {reason}.")
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, reason: Optional[str]):
        """Kicks a user"""
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't kick a higher up role.")
            await ctx.send(embed=embed) 
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't kick a same rank.")
            await ctx.send(embed=embed) 
        elif member == ctx.author:
            embed = discord.Embed(title=":x: You cannot kick yourself! If you are feeling/having suicidal/self-harm thoughts, visit https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines")
            await ctx.send(embed=embed)
        elif member == member.id(734822514894831639):
            embed = discord.Embed(title=":x: w-why do you want to kick me? What the heck did I do? :(")
            await ctx.send(embed=embed)
        else:
            await member.kick(reason=reason)
            embed = discord.Embed(title=f":white_check_mark: {member} was kicked; {reason}.")
            await ctx.send(embed=embed)
            
            try:
                channel = await member.create_dm()
                await channel.send(f'You were kicked in {ctx.guild.name} for {reason}.')
            except discord.HTTPException:
                embed = discord.Embed(title=f":white_check_mark: {member} was kicked; {reason}. I have recieved an error, so I cannot DM the user.")
                await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, reason: Optional[str]):
        """Warns a user"""
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't warn a higher up role.")
            return await ctx.send(embed=embed)
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't warn a same rank.")
            await ctx.send(embed=embed)  
        elif member == ctx.author:
            embed = discord.Embed(title=":x: You cannot warn yourself! If you are feeling/having suicidal/self-harm thoughts, visit https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines")
            return await ctx.send(embed=embed)
        elif member == member.id(734822514894831639):
            embed = discord.Embed(title=":x: w-why do you want to warn me? What the heck did I do? :(")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member} was warned; {reason}.")
            
            try:
                await member.send(f'You were warned in {ctx.guild.name} for {reason}.')
            except discord.HTTPException:
                await ctx.send(f':white_check_mark: {member} was warned; {reason}. I have recieved an error, so I cannot DM the user.')

    @commands.guild_only()
    @commands.command(name="purge")
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def purge(self, ctx, amount: int):
        """Mass deletes any messages. Cannot delete old messages (as in messages that are older then 14 days)"""
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title=f"I successfully deleted {amount} of messages.")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
    print('Moderation module loaded.')
