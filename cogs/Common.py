import pydoc

from discord.ext import commands, tasks
import discord
from Bot import Bot
from discord import Spotify
from googlesearch import search
import pprint
import ast


def safe_eval(expr, variables):
    """
    Safely evaluate a a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
    and None. safe operators are allowed (and, or, ==, !=, not, +, -, ^, %, in, is)
    """
    _safe_names = {'None': None, 'True': True, 'False': False}
    _safe_nodes = [
        'Add', 'And', 'BinOp', 'BitAnd', 'BitOr', 'BitXor', 'BoolOp',
        'Compare', 'Dict', 'Eq', 'Expr', 'Expression', 'For',
        'Gt', 'GtE', 'Is', 'In', 'IsNot', 'LShift', 'List',
        'Load', 'Lt', 'LtE', 'Mod', 'Name', 'Not', 'NotEq', 'NotIn',
        'Num', 'Or', 'RShift', 'Set', 'Slice', 'Str', 'Sub',
        'Tuple', 'UAdd', 'USub', 'UnaryOp', 'boolop', 'cmpop',
        'expr', 'expr_context', 'operator', 'slice', 'unaryop']
    node = ast.parse(expr, mode='eval')
    for subnode in ast.walk(node):
        subnode_name = type(subnode).__name__
        if isinstance(subnode, ast.Name):
            if subnode.id not in _safe_names and subnode.id not in variables:
                raise ValueError("Unsafe expression {}. contains {}".format(expr, subnode.id))
        if subnode_name not in _safe_nodes:
            raise ValueError("Unsafe expression {}. contains {}".format(expr, subnode_name))

    return eval(expr, variables)


def g_seach(args):
    search_args = (args, 1)
    gsearch = GoogleSearch()
    gresults = gsearch.search(*search_args)
    return gresults


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
        spotify = None
        for activity in member.activities:
            if isinstance(activity, Spotify):
                spotify = activity
            else:
                spotify = None
        if spotify is not None:
            track_url = f"https://open.spotify.com/track/{spotify.track_id}"
            embed = discord.Embed(title=spotify.title, type="rich", url=track_url, color=spotify.color)
            embed.set_footer(text=f"Requested for {member.name}", icon_url=member.avatar_url)
            embed.set_image(url=spotify.album_cover_url)
            embed.add_field(name="Album", value=spotify.album, inline=False)
            embed.add_field(name="Artist", value=spotify.artist, inline=False)
            embed.add_field(name="Duration", value=str(spotify.duration)[2:-7], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} ain't listening to anything. Send him some good shit.")

    #             await ctx.send(f"{user.mention} ain't listening to anything. Send him some good shit.")
    @commands.command()
    async def lmgtf(self, ctx, *, args: str):
        embed_msg = discord.Embed(title="Google search", description=f"Showing results for {args}", color=0x4885ed)
        i = 0
        for j in search(args, tld="com", num=5, stop=5, pause=0):
            i += 1
            embed_msg.add_field(name=str(i), value=j, inline=False)
        await ctx.send(embed=embed_msg)


def setup(bot: Bot):
    bot.add_cog(Common(bot))
