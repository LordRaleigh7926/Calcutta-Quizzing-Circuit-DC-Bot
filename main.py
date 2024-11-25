import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

# Import custom Var
from killList import kill_list
from pracList import prac
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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(f"{bot.user} is now online and ready!")


# Helper function to log messages to the log channel
async def log_message(message):
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(message)


# Reaction role feature
@bot.command(name="getRoles")
async def setup_roles(ctx):
    embed = discord.Embed(
        title="Choose Your Role by Reacting with the specified Emoji",
        description="\n".join([f"{emoji}:\t{role}\n" for emoji, role in reaction_roles.items()]),
        color=discord.Color.dark_purple(),
    )
    message = await ctx.send(embed=embed)
    print(reaction_roles)
    for emoji in list(reaction_roles.keys()): #reaction_roles:
        await message.add_reaction(str(emoji))
    await log_message(f"Role setup message created by {ctx.author} in {ctx.channel.mention}")



@bot.command(help="Returns kill statement of a person")
async def kill(ctx,*, name):
    
    kill_choice = random.choice(kill_list)

    await ctx.message.channel.send(f"{name} {kill_choice}")


@bot.command(name="prac", help="Returns prachurjo approved insults")
async def prachurjo(ctx):
    
    prac_choice = random.choice(prac)

    await ctx.message.channel.send(f"{prac_choice}")

@bot.command(name="ping", help="Gives the latency")
async def latency_check(ctx):
    await ctx.message.channel.send(f"Pong {round(bot.latency*1000)}ms")

@bot.command(name="purge", help="Clears the said number of messages. 🧹")
async def clear_messages(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@bot.event
async def on_raw_reaction_add(payload):
    
    print(f"Reaction added: {payload.emoji.name}")  # Debugging
    if payload.member == bot.user:
        return

    guild = bot.get_guild(payload.guild_id)
    role_name = reaction_roles.get(payload.emoji.name)
    if role_name:
        print(f"Found role: {role_name}")  # Debugging
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            await payload.member.add_roles(role)
            await log_message(f"Assigned {role_name} role to {payload.member} in {guild.name}")
        else:
            print(f"Role {role_name} not found in guild {guild.name}")
    else:
        print(f"No role found for emoji {payload.emoji.name}")


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role_name = reaction_roles.get(payload.emoji.name)
    if role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            await member.remove_roles(role)
            await log_message(f"Removed {role_name} role from {member} in {guild.name}")


# Censorship feature
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for word in prohibited_words:
        if word in message.content.lower():
            user = message.author
            await message.delete()
            await message.channel.send(f"{user.mention}, watch your language!")
            await log_message(
                f"Deleted message from {message.author.mention} in {message.channel.mention}\n"
                f"Content of Message: {message.content}\n"
                f"Number of warnings: {warnings.get(message.author.id, 0)+1}"
            )

            if user.id not in warnings:
                warnings[user.id] = 0
            warnings[user.id] += 1

            if warnings[user.id] >= warn_limit:
                guild = message.guild
                await guild.kick(user, reason="Excessive use of prohibited words.")
                await message.channel.send(f"{user.mention} has been kicked for using prohibited language.")
                await log_message(f"Kicked {user} for repeated prohibited language usage in {guild.name}")
            return

    await bot.process_commands(message)


# Run the bot
TOKEN = os.getenv("Token")
bot.run(TOKEN)
