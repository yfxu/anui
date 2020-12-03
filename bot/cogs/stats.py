import discord
import random
import sys
import os

from discord.utils import escape_markdown
from discord.ext import commands
from dotenv import load_dotenv

from .utils import db_utils
from .utils.embed_utils import AnuiEmbed

class Stats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name='profile')
	async def _profile(self, ctx, *, user: discord.Member = None):
		"""view Discord user's profile"""
		if user == None:
			user = ctx.message.author

		try:
			stats = db_utils.get_user(mongo_client=self.bot.mongo_client, user=user)
		except Exception as e:
			print(f"{__class__.__name__}: {e}")
			await ctx.send(f"could not generate a profile for `{user.display_name}`")
			return

		# create embed
		embed = AnuiEmbed().user_profile(user=user, stats=stats)
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
