import os
import discord
from Bot import Bot


def main():
    bot = Bot()

    @bot.event
    async def on_ready():
        activity = discord.Streaming(name=f"$help | {len(bot.guilds)} servers", url='https://www.twitch.tv/dashinsyo')
        await bot.change_presence(activity=activity)

    bot.load_extension(f"cogs.Admin")
    bot.run(os.environ['BOT_TOKEN'])


if __name__ == '__main__':
    main()
