from discord.ext import commands

class LatencyCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Gives the latency")
    async def latency_check(self, ctx):
        await ctx.send(f"Pong {round(self.bot.latency*1000)}ms")

async def setup(bot):
    await bot.add_cog(LatencyCheck(bot))
