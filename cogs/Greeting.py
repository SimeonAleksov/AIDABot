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
        await ctx.send(f"{member.mention}, my source code is here: https://github.com/SimeonAleksov/MerriBot")

    @commands.command()
    async def name(self, ctx, *, member: discord.Member = None):
        await ctx.send("Artificial Intelligent Digital Assistant (A.I.D.A.)\n "
                       "https://marvelcinematicuniverse.fandom.com/wiki/Aida")


def setup(bot: Bot):
    bot.add_cog(Greetings(bot))
