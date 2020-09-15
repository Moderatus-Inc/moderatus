import discord
from discord.ext import commands

class Moderation(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, reason):
        """
        Bans a user
        """
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't ban a higher up role.")
            await ctx.send(embed=embed)
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't kick a same rank.")
            await ctx.send(embed=embed) 
        elif member == ctx.author:
            embed = discord.Embed(title=":x: You cannot ban yourself! If you are feeling/having suicidal/self-harm thoughts, visit https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines")
            await ctx.send(embed=embed)
        else:   
            await member.ban()
            embed = discord.Embed(title=f":white_check_mark: {member} was banned; {reason}.")
            await ctx.send(embed=embed)
            channel = await member.create_dm()
            await channel.send(f'You were banned in {ctx.guild.name} for {reason}.')

    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unban(self, ctx, member: discord.Member, reason):
        """
        Unbans a user
        """
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            member = ban_entry.member
  
        if (member_name, member_discriminator) == (member_name, member_discriminator):
            await member.unban()
            embed = discord.Embed(title=f"{member} was unbanned; {reason}")
            await ctx.send(embed=embed)
            channel = await member.create_dm()
            await channel.send(f'You were unbanned in {ctx.guild.name} for {reason}.')
        elif member == None:
            embed = discord.Embed(title=":x: You need to sepcify a user!")
            await ctx.send(embed=embed) 


    @commands.command(name="mute")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member, reason):
        """
        Mutes a user
        """
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
            await ctx.add_roles(name="Muted", reason="Muted")
            channel = await member.create_dm()
            await channel.send(f'You were muted in {ctx.guild.name} for {reason}.')
            embed = discord.Embed(title=f":white_check_mark: {member} was muted; {reason}.")
            await ctx.send(embed=embed)

   
    @commands.command(name="unmute")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, reason):
        """
        Unmutes a user
        """   
        await discord.utils.get(name="Muted", permissions=discord.Permissions(send_messages=True, manage_messages=False))
        await ctx.remove_roles(name="Muted", reason="Unmuted")
        channel = await member.create_dm()
        await channel.send(f'You were unmuted in {ctx.guild.name} for {reason}.')
        embed = discord.Embed(title=f":white_check_mark: {member} was unmuted; {reason}.")
        await ctx.send(embed=embed)


    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, reason):
        """
        Kicks a user
        """
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't kick a higher up role.")
            await ctx.send(embed=embed) 
        elif member.top_role == ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't kick a same rank.")
            await ctx.send(embed=embed) 
        elif member == ctx.author:
            embed = discord.Embed(title=":x: You cannot kick yourself! If you are feeling/having suicidal/self-harm thoughts, visit https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines")
            await ctx.send(embed=embed)
        else:
            await member.kick()
            embed = discord.Embed(title=f":white_check_mark: {member} was kicked; {reason}.")
            await ctx.send(embed=embed)
            channel = await member.create_dm()
            await channel.send(f'You were kicked in {ctx.guild.name} for {reason}.')

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, reason):
        """
        Warns a user
        """
        if member.top_role > ctx.author.top_role:
            embed = discord.Embed(title="Nice try! You can't warn a higher up role.")
            return await ctx.send(embed=embed) 
        elif member == ctx.author:
            embed = discord.Embed(title=":x: You cannot warn yourself! If you are feeling/having suicidal/self-harm thoughts, visit https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines")
            return await ctx.send(embed=embed)
        else:
            await ctx.channel.send(f"{member} was warned; {reason}.")
            try:
                await member.send(f'You were warned in {ctx.guild.name} for {reason}.')
            except:
                return

    @commands.command(name="purge")
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def purge(self, ctx, amount):
        """
        Mass deletes any messages. Cannot delete more then 100 nor old messages (as in messages that are older then 14 days)
        """
        if amount > 100:
            embed = discord.Embed(title=f"You cannot delete more than 100 messages!")
        else:
            await ctx.channel.purge(limit = amount)
            embed = discord.Embed(title=f"I successfully deleted {amount} of messages.")
            await ctx.send(embed=embed)
            

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):

        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(exc, commands.CommandNotFound):
            return
        if isinstance(exc, commands.NotOwner):
            return await ctx.send("This command is locked to my owner only.")
        if isinstance(exc, commands.CommandInvokeError):
            ctx.command.reset_cooldown(ctx)
            exc = exc.original
        if isinstance(exc, commands.BadArgument):
            cleaned = discord.utils.escape_mentions(str(exc))
            return await ctx.send(cleaned)
        if isinstance(exc, commands.MissingPermissions):
            perms = "`" + '`, `'.join(exc.missing_perms) + "`" 
            return await ctx.send(f"You're missing {perms} permissions")
        if isinstance(exc, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(exc.missing_perms) + "`" 
            return await ctx.send(f"I'm missing {perms} permissions")
        if isinstance(exc, commands.CheckFailure):
            return
        if isinstance(exc, commands.TooManyArguments):
            if isinstance(ctx.command, commands.Group):
                return
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.send(f"You're missing required argument **{(exc.param.name)}**")
            return

def setup(bot):
    bot.add_cog(Moderation(bot))
    print('Moderation module loaded.')
