import discord

class AnuiEmbed():
	"""special embed templates for Anui bot"""
	def __init__(self):
		pass

	def user_user_action(self, sender, target, action="", emote="", mention_target=False):
		# user must be a discord user
		embed_title = ""
		embed_color = sender.color
		if mention_target:
			embed_desc = f"{emote} `{sender.display_name}` {action} {target.mention}! {emote}"			
		else:
			embed_desc = f"{emote} `{sender.display_name}` {action} `{target.display_name}`! {emote}"
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

	def user_profile(self, user, stats):
		profile_lines = []
		for stat in stats.keys():
			# get colon-delimited values within a stat
			stat_values_str = ':'.join(map(str, stats[stat].values()))
			profile_lines.append(f"▸ {stat} - `{stat_values_str}`")

		# make embed	
		embed_title = f"{user.display_name}'s profile"
		embed_desc  = "\n".join(profile_lines)
		embed_color = user.color
		embed_thumb = user.avatar_url

		embed = discord.Embed(title=embed_title, description=embed_desc, color=embed_color)
		embed.set_thumbnail(url=embed_thumb)
		return embed

