from discord.ext import commands
from Bot import Bot
import platform
import subprocess


class Ping(commands.Cog, name="Ping"):
    """Sandbox cog"""

    def __init__(self, bot: Bot):
        print("Ping cog loaded")
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context, site: str, packets: int):
        if packets > 10:
            packets = 1
            await ctx.send("don't be doin dat fam")
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, str(packets), site]
        msg = subprocess.check_output(command)
        msg = f"```{msg.decode()}```"
        await ctx.send(msg)


def setup(bot: Bot):
    bot.add_cog(Ping(bot))
