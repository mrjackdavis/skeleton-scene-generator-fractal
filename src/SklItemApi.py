import urllib.request
import logging
from nap.url import Url
from SklItem import SklItem

class SklItemApi:
	"""Skeleton Scene Item"""
	def __init__(self,url):
		self.apiUrl = url
		self.api = Url(self.apiUrl)

	def GetOne(self):
		# Get scenes
		scenes = self.api.get('scene').json()

		logging.debug(scenes)

		item = SklItem()

		item.resourceURL = scenes[0]['resource']['location']
		response = urllib.request.urlopen(item.resourceURL)
		item.resourceData = response.read().decode('utf-8')
		return item;