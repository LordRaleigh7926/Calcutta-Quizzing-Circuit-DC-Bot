import discord
from discord.ext import commands


# Channel ids
log_channel_id = 1310295248693497909
announcements_id = 1310295248693497909
bot_testing = 1310526721904214026

class OnRawReactionAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Helper function to log messages to the log channel
    async def log_message(self, message):
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            await log_channel.send(message)

    reaction_roles = {
        '👍': 'ThumbsUpRole',
        '👎': 'ThumbsDownRole'
        # Add more emoji-role mappings as needed
    }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(f"Reaction added: {payload.emoji.name}")  # Debugging
        if payload.member == self.bot.user:
            return

        guild = self.bot.get_guild(payload.guild_id)
        role_name = self.reaction_roles.get(payload.emoji.name)
        if role_name:
            print(f"Found role: {role_name}")  # Debugging
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await payload.member.add_roles(role)
                await self.log_message(f"Assigned {role_name} role to {payload.member} in {guild.name}")
            else:
                print(f"Role {role_name} not found in guild {guild.name}")
        else:
            print(f"No role found for emoji {payload.emoji.name}")

async def setup(bot):
    await bot.add_cog(OnRawReactionAdd(bot))