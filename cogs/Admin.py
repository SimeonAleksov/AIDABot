import os
from discord.ext import commands, tasks
from Bot import Bot
import discord
import asyncio
PROTECTED_COGS = ['Admin', ]


class Admin(commands.Cog, name="Admin"):
    """Bot admin cog"""

    def __init__(self, bot: Bot):
        print("Admin cog loaded")
        self.bot = bot
        self.load_all_cogs_task.start()

    # Tasks
    @tasks.loop(count=1)
    async def load_all_cogs_task(self):
        self.bot.load_all_cogs()

    @load_all_cogs_task.before_loop
    async def before_load_all_cogs_task(self):
        await self.bot.wait_until_ready()

    # Commands
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, extension: str):
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def load_all(self, ctx: commands.Context):
        self.bot.load_all_cogs()
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, extension: str):
        if extension not in PROTECTED_COGS:
            self.bot.unload_extension(f"cogs.{extension}")
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def unload_all(self, ctx: commands.Context):
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                await self.unload(ctx, filename[:-3])
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, extension: str):
        self.bot.reload_extension(f"cogs.{extension}")
        await ctx.message.add_reaction("✅")

    @commands.command(aliases=('r',))
    @commands.is_owner()
    async def reload_all(self, ctx: commands.Context):
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                await self.reload(ctx, filename[:-3])
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.has_role("Owner")
    async def purge(self, ctx: commands.Context, limit: int = 10):
        await ctx.channel.purge(limit=limit + 1)

    @commands.command()
    @commands.has_role("Owner")
    async def kick(self, ctx, member: discord.User, *, reason=None):
        await ctx.guild.kick(member, reason=reason)

    @commands.command()
    @commands.has_role("Owner")
    async def ban(self, ctx, member: discord.User, *, reason=None):
        await ctx.guild.ban(member, reason=reason)

    @commands.command()
    @commands.has_role("Owner")
    async def mute(self, ctx, member: discord.Member = None, *, mute_time: float):
        if member is None:
            await ctx.send('Pleasepass in a valid user')
            return
        guild_id = ctx.message.guild.id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
        role = discord.utils.get(guild.roles, name="Muted")
        noopy = discord.utils.get(guild.roles, name="NooPy")
        await member.add_roles(role)
        await member.remove_roles(noopy)
        await ctx.send(f'{member.mention} has been muted for {mute_time} seconds.')
        await asyncio.sleep(mute_time)
        await member.add_roles(noopy)
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} was unmuted!')


def setup(bot: Bot):
    bot.add_cog(Admin(bot))
