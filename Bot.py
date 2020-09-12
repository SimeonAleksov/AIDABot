import os

from discord.ext import commands
from discord.ext.commands import ExtensionAlreadyLoaded


class Bot(commands.Bot):
    def __init__(self):
        super(Bot, self).__init__(
            command_prefix=commands.when_mentioned_or("$"),
            case_insensitive=True,
            max_messages=10_000,
        )

    def load_all_cogs(self):
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f"cogs.{filename[:-3]}")
                except ExtensionAlreadyLoaded:
                    pass
