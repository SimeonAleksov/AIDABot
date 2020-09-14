from discord.ext import commands
import discord
from Bot import Bot


class Sandbox(commands.Cog, name="Rules"):
    """Rules cog"""

    def __init__(self, bot: Bot):
        print("Rules cog loaded")
        self.bot = bot

    @commands.command()
    @commands.has_role("Owner")
    async def rules(self, ctx: commands.Context):
        """Rules for this server"""
        rules_channel = self.bot.get_channel(747431013281562705)
        embed = discord.Embed(title="PyCord rules", type="rich", color=0x2471c7)
        embed.add_field(name="Rule #1", value="Be nice.", inline=False)
        embed.add_field(name="Rule #2", value="Be mature.", inline=False)
        embed.add_field(name="Rule #3", value="Follow the law.", inline=False)
        embed.add_field(name="Rule #4", value="Listen to the mods.", inline=False)
        embed.add_field(name="Rule #5",
                        value="Ask your question directly (https://dontasktoask.com/) and don't post across "
                              "multiple channels or ask people for programming help in DMs..", inline=False)
        embed.set_footer(text="React to this message to accept the rules, and you will be granted access to the rest "
                              "of the channels.")

        await rules_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 754343872099778580:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
            if payload.emoji.name == "yeah":
                role = discord.utils.get(guild.roles, name="NooPy")
            else:
                role = None
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.member.id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                else:
                    print("Member not found")
            else:
                print("Role not found")
        else:
            pass


def setup(bot: Bot):
    bot.add_cog(Sandbox(bot))
