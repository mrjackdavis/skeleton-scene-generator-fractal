import urllib.request
import logging
from nap.url import Url
from SklItem import SklItem

class SklItemApi:
	"""Skeleton Scene Item"""
	def __init__(self,url):
		self.apiUrl = url
		self.api = Url(self.apiUrl)

	def GetAllNew(self):
		# Get scenes
		scenes = self.api.get('scene').json()

		sceneObjs = []

		for scene in scenes:
			item = SklItem()

			item.resourceURL = scene['resource']['location']
			logging.info('Found item with resource location "%s"',item.resourceURL)

			response = urllib.request.urlopen(item.resourceURL)
			item.resourceData = response.read()

			sceneObjs.append(item)

		return sceneObjs;