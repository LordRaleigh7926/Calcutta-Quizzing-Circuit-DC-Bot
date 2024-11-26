from discord.ext import commands
import logging
import json
import os
from discord import Message, TextChannel, Guild, User


# Channel ids
log_channel_id = 1310295248693497909
announcements_id = 1310295248693497909
bot_testing = 1310526721904214026


class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    # Helper function to log messages to the log channel
    async def log_message(self, message):
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            await log_channel.send(message)

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author == self.bot.user:
            return
        warnings_file: str = "../../jsons/warnings.json"

        if os.path.exists(warnings_file):
            with open(warnings_file, "r") as f:
                warnings: dict[int, int] = json.load(f)
        else:
            warnings = {}

        warn_limit: int = 3
        prohibited_words = ["badword1", "badword2", "badword3"]
        for word in prohibited_words:
            if word in message.content.lower():
                user: User = message.author
                await message.delete()
                await message.channel.send(f"{user.mention}, watch your language!")
                await self.log_message(
                    f"Deleted message from {message.author.mention} in {message.channel.mention}\n"
                    f"Content of Message: {message.content}\n"
                    f"Number of warnings: {warnings.get(message.author.id, 0)+1}"
                )

                if user.id not in warnings:
                    warnings[user.id] = 0
                warnings[user.id] += 1

                if warnings[user.id] >= warn_limit:
                    guild: Guild = message.guild
                    await guild.kick(user, reason="Excessive use of prohibited words.")
                    await message.channel.send(f"{user.mention} has been kicked for using prohibited language.")
                    await self.log_message(self.bot, f"Kicked {user} for repeated prohibited language usage in {guild.name}")
                return

        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnMessage(bot))
