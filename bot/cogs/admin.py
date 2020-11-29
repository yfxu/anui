import os
import sys

import discord
from discord.ext import commands

admin_ids = [331686044699328512, 121395681742159875]

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	def is_admin(ctx):
		# load admin users file
		fname = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/users/admins.txt")
		f = open(fname, 'r')
		admin_ids = list(map(int, f.read().splitlines()))
		f.close()

		return ctx.message.author.id in admin_ids


	@commands.command(name='reload', hidden=True, pass_context=True)
	@commands.check(is_admin)
	async def _reload(self, ctx, *args):
		"""Reloads a module."""
		if len(args) == 0:
			await ctx.send(f"> no module to reload was given")
		else:
			try:
				module = "cogs." + args[0]
				self.bot.reload_extension(module)
			except Exception as e:
				print(e)
				await ctx.send(f"> `{module}` module could not be reloaded")
			else:
				await ctx.send(f"> `{module}` module successfully reloaded!")

	@_reload.error
	async def _reload_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			user = ctx.message.author
			print(f"{user} is not an admin", file=sys.stderr)


	@commands.command(name='load', hidden=True, pass_context=True)
	@commands.has_role("squishable")
	async def _load(self, ctx, *args):
		"""Loads a module."""
		if len(args) == 0:
			await ctx.send(f"> no module to reload was given")
		else:
			try:
				module = "cogs." + args[0]
				self.bot.load_extension(module)
			except Exception as e:
				print(e)
				await ctx.send(f"> `{module}` module could not be loaded")
			else:
				await ctx.send(f"> `{module}` module successfully loaded!")

	@_load.error
	async def _load_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			user = ctx.message.author
			print(f"{user} is not an admin", file=sys.stderr)


def setup(bot):
	bot.add_cog(Admin(bot))