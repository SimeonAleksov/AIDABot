from discord.ext import commands
import discord
from Bot import Bot
from discord import Spotify
import requests
from bs4 import BeautifulSoup
import autopep8


class Common(commands.Cog):
    def __init__(self, bot):
        print("Common cog loaded")
        self.bot = bot
        self._last_member = None
        self.message = None
        self.urls = []
        self.embed_msg = None
        self.query = ""

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
        """Links the source code for the bot"""
        member = member or ctx.author
        await ctx.send(f"{member.mention}, my source code is here: https://github.com/SimeonAleksov/AIDABot")

    @commands.command()
    async def name(self, ctx, *, member: discord.Member = None):
        await ctx.send("Artificial Intelligent Digital Assistant (A.I.D.A.)")

    @commands.command()
    @commands.has_role("Manager")
    async def latency(self, ctx):
        """Prints the latency for the bot"""
        await ctx.send(f"My latency is: `{self.bot.latency}`")

    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        """Information about a song that user is listening"""
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

    @commands.command()
    async def docs(self, ctx, *, args: str):
        r = requests.get('https://docs.devdocs.io/python~3.8/db.json?1578588615')
        try:
            soup = BeautifulSoup(r.json()[f'library/{args}'], 'html.parser')
        except:
            soup = None
        if soup is not None:
            embed = discord.Embed(title=f"Showing results for {args}", type="rich")
            dl = soup.find_all('dl', {'class': 'function'})
            para = ""
            for item in dl[:5]:
                try:
                    lnk = item.dd.p('a')[0]['href']
                except:
                    lnk = ''
                try:
                    code = item.dd.pre.text
                except:
                    code = ""
                if code:
                    para += item.dd.p.text + "\n"
                    para += f"```{code}```"
                else:
                    para = item.dd.p.text
                embed.add_field(name=item.code.text, value=para, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Not found.")

    @commands.command()
    async def code(self, ctx, member: discord.Member = None):
        """Shows how to format a code in a discord message"""
        member = member or ctx.author
        embed = discord.Embed(title="Code formatting", type="rich")
        msg = """\```language_name
# code here
\```
"""
        example = """
        \```python
if True:
    print("Hi!")
\```"""
        output = """
                ```python
if True:
    print("Hi!")```"""
        embed.add_field(name="Format", value=msg, inline=False)
        embed.add_field(name="Example", value=example, inline=False)
        embed.add_field(name="Output", value=output, inline=False)
        embed.set_footer(text=f"Requested for {member.display_name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, page='Help'):
        """Get help with a command or cog

        eg. `$help user`"""
        page = page.capitalize()
        all_cogs = '`, `'.join([c for c in self.bot.cogs])
        color = discord.Colour.green()
        if page in all_cogs:
            embed = discord.Embed(title=f'Help with {page} commands',
                                  description=self.bot.cogs[page].__doc__, color=color)

            embed.add_field(name=f'The current loaded cogs are (`{all_cogs}`) :gear:', value=f'**Bot Description**: '
                                                                                             f'{self.bot.description}')

            for c in self.bot.get_cog(page).get_commands():
                if await c.can_run(ctx):
                    if len(c.signature) == 0:
                        command = f'`{self.bot.prefix}{c.name}`'
                    else:
                        command = f'`{self.bot.prefix}{c.name} {c.signature}`'
                    if len(c.short_doc) == 0:
                        message = 'There is no documentation for this command'
                    else:
                        message = c.short_doc
                    embed.add_field(name=command, value=message, inline=False)
        else:
            all_commands = [c.name for c in self.bot.commands if await c.can_run(ctx)]
            page_lo = page.lower()
            if page_lo in all_commands:
                embed = discord.Embed(title=f'Help with the {self.bot.get_command(page_lo)}` command', color=color)
                if len(self.bot.get_command(page_lo).help) == 0:
                    message = 'There is no documentation for this command'
                else:
                    message = self.bot.get_command(page_lo).help
                embed.add_field(name='Documentation:', value=message)

                if len(self.bot.get_command(page_lo).signature) != 0:
                    args = self.bot.get_command(page_lo).signature
                    embed.add_field(name='Arguments', value=f'`{args}`')
            else:
                embed = discord.Embed(title='Error!',
                                      description=f'**Error 404:** Command or Cog \"{help}\" not found ¯\_(ツ)_/¯',
                                      color=discord.Color.red())
                embed.add_field(name=f'Current loaded Cogs are (`{all_cogs}`) :gear:', value='\u200b')

        await ctx.send(embed=embed)

    @commands.command()
    async def format(self, ctx, lang: str):
        await ctx.channel.purge(limit=1)
        messages = await ctx.channel.history(limit=1).flatten()
        msg = await ctx.channel.fetch_message(messages[0].id)
        formatted = f"```{lang}\n" \
                    f"{autopep8.fix_code(msg.content)}" \
                    f"```"
        await ctx.send(formatted)


def setup(bot: Bot):
    bot.add_cog(Common(bot))
