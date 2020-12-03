import asyncio
import random
import sys
import os
import re
from dotenv import load_dotenv

from .utils import db_utils
from .utils import file_utils
from .utils.embed_utils import AnuiEmbed

from .utils.mapquest import Mapquest

import discord
from discord.utils import escape_markdown
from discord.ext import commands

import pymongo

import geopy.distance

load_dotenv()
MONGO_URI    = os.getenv('MONGO_URI')
MAPQUEST_KEY = os.getenv('MAPQUEST_KEY')

mongo_client = pymongo.MongoClient(MONGO_URI)
min_game_duration = 15

class Games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def __del__(self):
		mongo_client.close()

	def latlong_format(self, content):
		try:
			# split any non-alphanumeric characters
			vals = re.split('\W+', content)
			lat  = float(vals[0].strip())
			lng  = float(vals[1].strip())

			if lat <= 90 and lat > -90 and lng > -180 and lng <= 180:
				return (lat, lng)
		except Exception as e:
			print(f"latlong_format() exception: {e}")
			return None

	@commands.command(name='game')
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.guild)
	async def _game(self, ctx, game):
		"""play a minigame!"""
		duration = 20

		if game.lower() in ['latlong', 'll']:
			api = Mapquest(MAPQUEST_KEY)
			location_strs = file_utils.get_data('/games/latlong/locations.txt')
			location_str  = random.choice(location_strs)

			# fetch geolocation stats and send START GAME embed
			location_data = await api.get_geocoding(location_str)
			results       = location_data['results'][0]
			location_str  = results['providedLocation']['location']
			location_url  = results['locations'][0]['mapUrl'].split('|')[0]
			start_embed   = AnuiEmbed().latlong_start(location=location_str, duration=duration, url=location_url)
			start_message = await ctx.send(embed=start_embed)

			latitude_longitude = results['locations'][0]['latLng']
			location_coords    = (latitude_longitude['lat'], latitude_longitude['lng']) 

			# wait for responses			
			await asyncio.sleep(duration)

			# calculate distances
			answers = {}
			async for m in ctx.history(after=start_message):
				answer = self.latlong_format(m.content)
				if answer is not None:
					answers[m.author.mention] = geopy.distance.distance(answer, location_coords).km

			# display results
			leaderboard      = sorted(answers.items(), key=lambda x: x[1])
			scoreboard_embed = AnuiEmbed().latlong_scoreboard(leaderboard=leaderboard, location=location_str, url=location_url)
			await ctx.send(embed=scoreboard_embed)

	@_game.error
	async def _game_error(self, ctx, error):
		"""game command error handler"""
		print(f"ERROR NOT HANDLED: {error}", file=sys.stderr)




# handle cog setup and cleanup
def setup(bot):
	bot.add_cog(Games(bot))

def teardown(bot):
	mongo_client.close()
