import re
import asyncio

from . import db_utils

class MsgAnalyzer():
	"""docstring for MsgAnalyzer"""
	def __init__(self, mongo_client):
		self.client = mongo_client

	async def xd_counter(self, message):
		user    = message.author
		content = message.content

		xd_count = len(re.findall(pattern="xd", string=content, flags=re.IGNORECASE))
		if xd_count > 0:
			db_utils.stats_increment(mongo_client=self.client, user=user, field='xd.count', value=xd_count)
