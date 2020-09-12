from discord.ext import commands, tasks
import discord
from Bot import Bot


class Greetings(commands.Cog):
    def __init__(self, bot):
        print("Greetings cog loaded")
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        rules_channel = self.bot.get_channel(747431013281562705)
        role = discord.utils.get(member.guild.roles, name='NooPy')
        await member.add_roles(role)

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


def setup(bot: Bot):
    bot.add_cog(Greetings(bot))
