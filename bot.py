import discord
import logging
from discord.ext import commands, tasks
from datetime import datetime, time
import random
import csv
import re
import asyncio
import os
import json

print("UTC Time:", datetime.utcnow())
print("System Local Time:", datetime.now())
print("Time zone offset (hours):", (datetime.now() - datetime.utcnow()).total_seconds)
# Configure logging
logging.basicConfig(
    filename=r"bot_errors.log",  # Name of the log file
    level=logging.INFO,        # Log only errors and above
    format='%(asctime)s - %(levelname)s - %(message)s'
)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!scatman ', intents=intents)
MESSAGE_TIMES = [
    {"hour": 14, "minute": 0},  # Example: time to send messages
]

import csv
with open(r"scatman/Scatman Jogn Lyrics.csv", encoding='utf-8') as f:
    lyrics = list(csv.DictReader(f))
channels_file = r'scatman/channels.json'


def load_channels():
    if not os.path.exists(channels_file):
        logging.warning("channels.json not found, creating new one.")
        return {}
    try:
        with open(channels_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error("channels.json is corrupted or not valid JSON.")
        return {}
    
def save_channels(data):
    with open(channels_file, 'w') as f:
        json.dump(data, f, indent=2)

def clean(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)  # Optional: remove punctuation
    return text

cleaned_lyric_lookup = {}

for row in lyrics:
    cleaned = clean(row['Lyric'])
    cleaned_lyric_lookup[cleaned] = (row['Lyric'], row['Song'])

@tasks.loop(hours=1)
async def generate_random_lyric():
    
    global random_row
    random_row = random.choice(lyrics)
    print("generated")
    
    now = datetime.now().time()  # Get current time as a datetime object
    logging.info(f"Generated random lyric at: {now}")


@tasks.loop(seconds=45)  # Check every 45 seconds
async def send_daily_lyric():
    now = datetime.now().time()  # Get current time as a datetime object
    logging.debug(f"Current time: {now}")  # Print the current time
    # Check if the current time matches any of the MESSAGE_TIMES
    for time in MESSAGE_TIMES:
        # Check if the current time matches the hour and minute from MESSAGE_TIMES
        if now.hour == time["hour"] and now.minute == time["minute"]:
            for guild in bot.guilds:
                # Find the target channel by name
                channels = load_channels()
                channel = bot.get_channel(channels[str(guild.id)])


                if channel is None:
                    logging.error(f"Error: Channel not found in '{guild.name}'. Skipping this server.")
                    
                    continue  # Skip this guild if the channel is not found
                message = f"{random_row['Lyric']}"

                 # Send the message to the channel
                await channel.send(message)
                
                logging.info(f"Sent verse at {now} to channel '{channel.name}' in guild '{guild.name}'")

            await asyncio.sleep(60)
            # No need for return, continue to check other servers after sending
            break  # Exit the loop after sending the verse at the correct time    
                
@bot.event
async def on_ready():
    print(f'Bot ready as {bot.user}')
    print(f'Commands loaded: {[cmd.name for cmd in bot.commands]}')
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    if not generate_random_lyric.is_running():
        generate_random_lyric.start()

    if not send_daily_lyric.is_running():
        send_daily_lyric.start()

logging.info('------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I couldn't keep that face up if I tried.")

@bot.command()
async def ping(ctx):
    await ctx.send("I'm the Scatman.")

@bot.command()
async def lyric(ctx):
    await ctx.send(f"Today's lyric is from {random_row['Song']}")

@bot.command()
async def randomlyric(ctx):
    row = random.choice(lyrics)
    message = f"{row['Lyric']}"
    await ctx.send(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    channels = load_channels()
    guild_id = str(ctx.guild.id)

    channels[guild_id] = ctx.channel.id

    save_channels(channels)
    await ctx.send(f"{ctx.channel.mention} is now Scatman's World.")
    logging.info(f"Set channel for guild {guild_id} to {ctx.channel.id}")

bot.remove_command("help")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Scatman John",
        description="",
        color=discord.Color.lighter_grey()
    )

    embed.add_field(
        name="!scatman lyric",
        value="Display the song today's lyric is from",
        inline=False
    )
    embed.add_field(
        name="!scatman setup",
        value="Assign the channel this command is sent in as the one Scatman John will talk. Only admins can use this",
        inline=False
    )
    embed.add_field(
        name="!scatman help",
        value="Displays this page",
        inline=False
    )
    embed.add_field(
        name="!scatman randomlyric",
        value="Says a random Scatman John Lyric",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == bot.user:
        return
    
    user_msg = clean(message.content)

    if user_msg in cleaned_lyric_lookup:
        original_lyric, song = cleaned_lyric_lookup[user_msg]
        await message.channel.send(f'"{original_lyric}" is a lyric in **{song}**')

    # Process commands if any
    await bot.process_commands(message)
f = open("grok.txt","r")
txt = f.read("grok.txt")
bot.run(txt.strip())