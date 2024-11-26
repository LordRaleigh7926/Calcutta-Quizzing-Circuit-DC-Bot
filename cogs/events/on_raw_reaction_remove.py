import discord
from discord.ext import commands

# Channel ids
log_channel_id = 1310295248693497909
announcements_id = 1310295248693497909
bot_testing = 1310526721904214026
class OnRawReactionRemove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.reaction_roles: dict[str, str] = {
            '👍': 'ThumbsUpRole',
            '👎': 'ThumbsDownRole'
            # Add other emoji-role mappings here
        }
    # Helper function to log messages to the log channel
    async def log_message(self, message):
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            await log_channel.send(message)
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> None:
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        member: discord.Member = guild.get_member(payload.user_id)
        role_name: str = self.reaction_roles.get(payload.emoji.name)
        if role_name:
            role: discord.Role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.remove_roles(role)
                await self.log_message(f"Removed {role_name} role from {member} in {guild.name}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnRawReactionRemove(bot))
