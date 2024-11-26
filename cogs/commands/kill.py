import discord
from discord.ext import commands
import random
from killList import kill_list

class Kill(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kill')
    async def kill(self, ctx, *, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to specify a member to kill.")
            return

        kill_message = random.choice(kill_list)
        await ctx.send(f"{member.display_name} {kill_message}")

async def setup(bot):
    await bot.add_cog(Kill(bot))
