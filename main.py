import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from schoolList import getSchoolList, getSchoolRolesDict


load_dotenv()


# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="- ", intents=intents)

# Load cogs
cogs = [
    "cogs.events.on_message",
    "cogs.events.on_raw_reaction_add",
    "cogs.events.on_raw_reaction_remove",
    "cogs.commands.prachurjo",
    "cogs.commands.latency_check",
    "cogs.commands.clear_messages",
    "cogs.commands.kill",
]



# Configuration
schoolList = getSchoolList()
schoolRolesEmojis = getSchoolRolesDict()
reaction_roles = schoolRolesEmojis

prohibited_words = ["badword1", "badword2", "badword3"]
warn_limit = 10
warnings = {}


# Channel ids
log_channel_id = 1310295248693497909
announcements_id = 1310295248693497909
bot_testing = 1310526721904214026

# Helper function to log messages to the log channel
async def log_message(message):
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(message)

@bot.event
async def on_ready():
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"Loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")
            await log_message(f"Failed to load cog {cog}: {e}")
    print(f"Logged in as {bot.user}")
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(f"{bot.user} is now online and ready!")




# Run the bot
TOKEN = os.getenv("Token")
bot.run(TOKEN)
