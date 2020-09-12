from discord.ext import commands, tasks
import discord
from Bot import Bot
from discord import Spotify


class Common(commands.Cog):
    def __init__(self, bot):
        print("Common cog loaded")
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        rules_channel = self.bot.get_channel(747431013281562705)
        if channel is not None:
            await channel.send(f'Hello {member.mention}, please read the {rules_channel.mention}')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.mention}~')
        else:
            await ctx.send(f'Hello {member.mention}... This feels familiar.')
        self._last_member = member

    @commands.command()
    async def source(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"{member.mention}, my source code is here: https://github.com/SimeonAleksov/AIDABot")

    @commands.command()
    async def name(self, ctx, *, member: discord.Member = None):
        await ctx.send("Artificial Intelligent Digital Assistant (A.I.D.A.)")

    @commands.command()
    @commands.has_role("Owner")
    async def kick(self, ctx, member: discord.User, *, reason=None):
        await ctx.guild.kick(member, reason=reason)

    @commands.command()
    @commands.has_role("Owner")
    async def ban(self, ctx, member: discord.User, *, reason=None):
        await ctx.guild.ban(member, reason=reason)

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        member = user or ctx.author
        for activity in member.activities:
            if isinstance(activity, Spotify):
                await ctx.send(f"{member.mention} is listening to **{activity.title}** by **{activity.artist}**")


def setup(bot: Bot):
    bot.add_cog(Common(bot))
