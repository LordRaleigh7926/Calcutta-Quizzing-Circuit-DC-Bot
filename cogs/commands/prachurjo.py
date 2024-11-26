import random
from discord.ext import commands
from pracList import prac

class Prachurjo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="prac", help="Returns prachurjo approved insults")
    async def prachurjo(self, ctx: commands.Context) -> None:
        prac_choice: str = random.choice(prac)
        await ctx.message.channel.send(f"{prac_choice}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Prachurjo(bot))
