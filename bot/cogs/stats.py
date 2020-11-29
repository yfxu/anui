import discord
import pymongo
import random
import sys
import os
from discord.utils import escape_markdown
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

mongo_client = pymongo.MongoClient(MONGO_URI)

class Stats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name='profile')
	async def _profile(self, ctx, *, user: discord.Member = None):
		"""view Discord user's profile"""
		if user == None:
			user = ctx.message.author

		try:
			client = mongo_client['stats']['users']
			r = client.find_one({'user': user.id})

			sneks_received = 0
			sneks_sent     = 0
			smaks_received = 0
			smaks_sent     = 0

			if r is not None:
				if 'sneks' in r:
					if 'send_count' in r['sneks']:
						sneks_sent = r['sneks']['send_count']
					if 'recv_count' in r['sneks']:
						sneks_received = r['sneks']['recv_count']
				if 'smaks' in r:
					if 'send_count' in r['smaks']:
						smaks_sent = r['smaks']['send_count']
					if 'recv_count' in r['smaks']:
						smaks_received = r['smaks']['recv_count']

		except Exception as e:
			print(e)
			await ctx.send(f"could not generate a profile for `{user.display_name}`")
			return

		# create embed
		embed_title = f"{user.display_name}'s profile"
		embed_color = user.color
		embed_thumb = user.avatar_url
		embed_field_sneks = {
			'name'   : 'sneks',
			'value'  : f"sent: `{sneks_sent:,}`\nreceived: `{sneks_received:,}`",
			'inline' : False
		}
		embed_field_smaks = {
			'name'   : 'smaks',
			'value'  : f"sent: `{smaks_sent:,}`\nreceived: `{smaks_received:,}`",
			'inline' : False
		}
		embed=discord.Embed(title=embed_title, color=embed_color)
		embed.add_field(**embed_field_sneks)
		embed.add_field(**embed_field_smaks)
		embed.set_thumbnail(url=embed_thumb)

		await ctx.send(embed=embed)

	@_profile.error
	async def _profile_error(self, ctx, error):
		if isinstance(error, commands.MemberNotFound):
			user = error.argument
			await ctx.send(f"> user `{user}` could not be found")

# handle cog setup and cleanup
def setup(bot):
	bot.add_cog(Stats(bot))

def teardown(bot):
	mongo_client.close()
