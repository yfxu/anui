import random
import sys
import os
from dotenv import load_dotenv

from .utils import db_utils
from .utils import file_utils
from .utils.embed_utils import AnuiEmbed

import discord
from discord.utils import escape_markdown
from discord.ext import commands

class Squish(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command(name='snek')
	async def _snek(self, ctx, user: discord.Member):
		"""sneks a user!"""

		# load sneks emotes
		emotes = file_utils.get_data('/emotes/snek.txt')
		emote  = random.choice(emotes)
		target = user
		sender = ctx.message.author

		if target == sender:
			await ctx.send(f"> you can't snek yourself stupid fuck")
			return

		# create and send embed
		embed = AnuiEmbed().user_user_action(sender=sender, target=target, action="sneks", emote=emote)
		await ctx.send(embed=embed)

		# update sneks in database
		try:
			db_utils.stats_increment(mongo_client=self.bot.mongo_client, user=sender, field='sneks.send_count')
			db_utils.stats_increment(mongo_client=self.bot.mongo_client, user=target, field='sneks.recv_count')
		except Exception as e:
			print(f"{e}: sneks could not be incremented", file=sys.stderr)

	@_snek.error
	async def _snek_error(self, ctx, error):
		"""snek command error handler"""
		if isinstance(error, commands.MissingRequiredArgument):
			user = ctx.message.author.display_name
			await ctx.send(f"> `{user}` sneks nothing!")
		elif isinstance(error, commands.CommandOnCooldown):
			time_remaining = round(error.retry_after, 2)
			await ctx.send(f"> you gotta wait `{time_remaining}s` before you may snek again")
		elif isinstance(error, commands.MemberNotFound):
			user = error.argument
			await ctx.send(f"> user `{user}` could not be found")
		else:
			print(f"ERROR NOT HANDLED: {error}", file=sys.stderr)


	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command(name='smak')
	async def _smak(self, ctx, user: discord.Member):
		"""smaks a user!"""

		# load smaks emotes
		emotes = file_utils.get_data('/emotes/smak.txt')
		emote  = random.choice(emotes)
		action = random.choice(['smaks', 'claps', 'brutalizes', 'stomps on', 'belittles', 'makes fun of', 'shits on', 'ends'])
		target = user
		sender = ctx.message.author

		# create and send embed
		if target != sender:
			embed = AnuiEmbed().user_user_action(sender=sender, target=target, action=action, emote=emote)
		else:
			action = random.choice([
				"smaks themselves brutally",
				"beats themself up over nothing",
				"hates themself!!"
			])
			embed = AnuiEmbed().user_action(sender=sender, action=action, emote=emote)
		await ctx.send(embed=embed)

		# update smaks in database
		try:
			db_utils.stats_increment(mongo_client=self.bot.mongo_client, user=sender, field='smaks.send_count')
			db_utils.stats_increment(mongo_client=self.bot.mongo_client, user=target, field='smaks.recv_count')
		except Exception as e:
			print(f"{e}: smaks could not be incremented", file=sys.stderr)

	@_smak.error
	async def _smak_error(self, ctx, error):
		"""smak command error handler"""
		if isinstance(error, commands.MissingRequiredArgument):
			user = ctx.message.author.display_name
			await ctx.send(f"> `{user}` smaks nothing!")
		elif isinstance(error, commands.CommandOnCooldown):
			time_remaining = round(error.retry_after, 2)
			await ctx.send(f"> you gotta wait `{time_remaining}s` before you may smak again")
		elif isinstance(error, commands.MemberNotFound):
			user = error.argument
			await ctx.send(f"> user `{user}` could not be found")
		else:
			print(f"ERROR NOT HANDLED: {error}", file=sys.stderr)


	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command(name='poke')
	async def _poke(self, ctx, user: discord.Member):
		"""pokes a user!"""

		emote  = ":point_right:"
		action = "pokes"
		target = user
		sender = ctx.message.author

		# create and send embed
		if target == sender:
			await ctx.send(f"> you cannot poke yourself!")
			return
		else:
			embed = AnuiEmbed().user_user_action(sender=sender, target=target, action=action, emote=emote, mention_target=True)
			await ctx.send(embed=embed)

	@_poke.error
	async def _poke_error(self, ctx, error):
		"""poke command error handler"""
		if isinstance(error, commands.MissingRequiredArgument):
			user = ctx.message.author.display_name
			await ctx.send(f"> `{user}` pokes nothing!")
		elif isinstance(error, commands.CommandOnCooldown):
			time_remaining = round(error.retry_after, 2)
			await ctx.send(f"> you gotta wait `{time_remaining}s` before you may poke again")
		elif isinstance(error, commands.MemberNotFound):
			user = error.argument
			await ctx.send(f"> user `{user}` could not be found")
		else:
			print(f"ERROR NOT HANDLED: {error}", file=sys.stderr)


	@commands.cooldown(1, 60, commands.BucketType.user)
	@commands.command(name='harass')
	async def _harass(self, ctx, user: discord.Member, times: int = 10):
		"""harasses a user a maximum of 20 times"""

		# bound <times> to range [1, 20]
		times  = max(1, min(times, 20))
		target = user

		for i in range(times):
			await ctx.send(user.mention)

	@_harass.error
	async def _harass_error(self, ctx, error):
		"""harass command error handler"""
		if isinstance(error, commands.MissingRequiredArgument):
			user = ctx.message.author.display_name
			await ctx.send(f"> harass failed")
		elif isinstance(error, commands.CommandOnCooldown):
			time_remaining = round(error.retry_after, 2)
			await ctx.send(f"> you gotta wait `{time_remaining}s` before you may harass someone again")
		elif isinstance(error, commands.MemberNotFound):
			user = error.argument
			await ctx.send(f"> user `{user}` could not be found")
		else:
			print(f"ERROR NOT HANDLED: {error}", file=sys.stderr)


def setup(bot):
	bot.add_cog(Squish(bot))
