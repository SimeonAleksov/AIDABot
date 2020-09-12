import os
import discord
from Bot import Bot


def main():
    bot = Bot()

    @bot.event
    async def on_ready():
        activity = discord.Game(name="$help")
        await bot.change_presence(activity=activity)

    bot.load_extension(f"cogs.Admin")
    bot.run(os.environ["BOT_TOKEN"])


if __name__ == '__main__':
    main()
