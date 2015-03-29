import urllib.request

class SklItem:
	"""Skeleton Scene Item"""
	def __init__(self,sceneId,resourceURL):
		self.id = sceneId
		self.processes = []
		self.resourceURL = resourceURL

	def GetData(self):
		response = urllib.request.urlopen(self.resourceURL)
		return response.read()
