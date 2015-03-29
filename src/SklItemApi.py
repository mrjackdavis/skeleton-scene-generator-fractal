import urllib.request
import logging
import json
from nap.url import Url
from SklItem import SklItem
from SklProcess import SklProcess

class SklItemApi:
	"""Skeleton Scene Item"""
	def __init__(self,url):
		self.apiUrl = url
		self.api = Url(self.apiUrl)
		self.jsonHeader = {'Content-type': 'application/json'}

	def GetAllNew(self):
		# Get scenes
		scenes = self.api.get('scene').json()

		sceneObjs = []

		for scene in scenes:
			item = SklItem(scene['_id'])

			item.resourceURL = scene['resource']['location']
			logging.info('Found item with resource location "%s"',item.resourceURL)

			try:
				response = urllib.request.urlopen(item.resourceURL)
				item.resourceData = response.read()

				sceneObjs.append(item)
				pass
			except:
				logging.warning('Unable to retrieve data for request %s',item.id)
				pass

		return sceneObjs

	def StartProcessing(self, sklItem):
		response = self.api.post('scene/%s/processes' % (sklItem.id), data=json.dumps({'status': 'InProgress'}),headers=self.jsonHeader)
		
		if response.status_code != 201:
			raise Exception('Creating a new process in the skeleton API failed. Received %s status code',response.status_code)

		processId = response.headers["location"].rsplit('/',1)[1];

		logging.debug("Starting process %s",response.headers["location"])

		return SklProcess(processId,sklItem)

	# def FailProcessing(self,process):
	# 	response = self.api.put('scene/%s/processes/%s' % (sklItem.processes), data={'status': 'Failed'})
	# 	logging.debug(response)

	def CompleteProcessing(self,sklProcess):
		processUrl = 'scene/%s/processes/%s' % (sklProcess.sklItem.id,sklProcess.id)
		logging.debug('Marking process %s as complete',processUrl)

		response = self.api.put(processUrl, data=json.dumps({'status': 'Complete','result': '%s.png' % (sklProcess.sklItem.id)}),headers=self.jsonHeader)

		if response.status_code != 200:
			raise Exception('Completing item %s, process %s; failed with status code %s' % (sklProcess.sklItem.id,sklProcess.id,response.status_code))

		logging.debug(response)