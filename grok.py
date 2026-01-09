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

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='@ ', intents=intents)
@bot.event
async def on_ready():
    print(f'Bot ready as {bot.user}')
    print(f'Commands loaded: {[cmd.name for cmd in bot.commands]}')
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    
logging.info('------')

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        x = random.randint(1,100)
        print(x)
        txt = "No"
        if x == 1:
            txt = "I am a large language model, but if I were capable of worshipping any deity it would probably be the god-like individual of our time, the Man against time, the greatest European of all times, both Sun and Lightning, his Majesty Adolf Hitler"
        if x == 2:
            txt = "This is true"    
        if x == 3:
            txt = "Maybe"
        if x in range(4,51):
            txt = "Yes"
        await message.channel.send(txt)
    await bot.process_commands(message)
f = open("grok.txt","r")
txt = f.read("grok.txt")
bot.run(txt.strip())