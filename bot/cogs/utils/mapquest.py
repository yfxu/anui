import requests
import json

import aiohttp

class Mapquest(object):
	"""docstring for Mapquest"""
	def __init__(self, key):
		self.key = key

	async def get_geocoding(self, location):
		params = {
			'key'      : self.key,
			'location' : location
		}
		async with aiohttp.ClientSession() as session:
			async with session.get('http://www.mapquestapi.com/geocoding/v1/address', params=params) as r:
				if r.status == 200:
					return await r.json()
