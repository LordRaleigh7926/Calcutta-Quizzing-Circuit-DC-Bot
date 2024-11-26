from discord.ext import commands

class ClearMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", help="Clears the said number of messages. 🧹")
    async def clear_messages(self, ctx, amount=5):
        if ctx.guild and ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            try:
                deleted = await ctx.channel.purge(limit=amount+1)
                if deleted is None:
                    await ctx.send("No messages were deleted.")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
        else:
            await ctx.send("I do not have permission to manage messages.")

async def setup(bot):
    await bot.add_cog(ClearMessages(bot))