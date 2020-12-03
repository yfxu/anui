# Anui bot
# 安慰 (Ān wèi)
#  - comfort (noun)
#     1. a state of physical ease and freedom from pain or constraint.
#     2. the easing or alleviation of a person's feelings of grief or distress.

import os
import sys

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

from cogs.utils.msg_utils import MsgAnalyzer

import discord
import pymongo

# load env variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI     = os.getenv('MONGO_URI')

# create bot
bot  = commands.Bot(command_prefix="!")

# connect to MongoDB
mongo_client     = pymongo.MongoClient(MONGO_URI)
bot.mongo_client = mongo_client

# create message analyzer
msga = MsgAnalyzer(bot.mongo_client)

# extensions for commands found in cogs folder
extensions = [
	'cogs.admin',
	'cogs.squish',
	'cogs.stats',
	'cogs.games'
]

if __name__ == '__main__':
	for extension in extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print(f"{e}: failed to load extension {extension}")

@bot.event
async def on_message(message):
	if message.author != bot.user:
		try:
			await bot.process_commands(message)
		except Exception as e:
			print(e, file=sys.stderr)

		await msga.xd_counter(message)


@bot.event
async def on_ready():
	print( f'{bot.user} has connected to Discord!' )

bot.run( DISCORD_TOKEN, bot=True, reconnect=True )
