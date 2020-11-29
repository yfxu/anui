import discord

class Anui_Embed():
	"""special embed templates for Anui bot"""
	def __init__(self):
		pass

	def user_user_action(self, sender, target, action="", emote=""):
		# user must be a discord user
		embed_title = ""
		embed_desc  = f"{emote} `{sender.display_name}` {action} `{target.display_name}`! {emote}"
		embed_color = sender.color
		return discord.Embed(title=embed_title, description=embed_desc, color=embed_color)

	def user_action(self, sender, action="", emote=""):
		# user must be a discord user
		embed_title = ""
		embed_desc  = f"{emote} `{sender.display_name}` {action}! {emote}"
		embed_color = sender.color
		return discord.Embed(title=embed_title, description=embed_desc, color=embed_color)

	def latlong_start(self, location, duration, url):
		embed_title = f"latlong! - {location}"
		embed_desc  = f"Guess the correct latitude and longitude of **{location}** within {duration} seconds!"
		embed_color = 0x4a93ff
		embed = discord.Embed(title=embed_title, description=embed_desc, color=embed_color)
		embed.set_image(url=url)
		return embed

	def latlong_scoreboard(self, leaderboard, location, url):
		embed_title = f"Time's up!"
		embed_desc  = "\n".join([ f"{score[0]} > `{round(score[1], 2):,}km`" for score in leaderboard ])
		embed_color = 0x4a93ff
		embed = discord.Embed(title=embed_title, description=embed_desc, color=embed_color)
		embed.set_image(url=url)
		return embed