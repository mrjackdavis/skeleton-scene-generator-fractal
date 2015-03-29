import os
import time
import generator
import logging
from SklItemApi import SklItemApi

logging.basicConfig(level=logging.DEBUG)

# Get API URL from environment
apiLocation = os.environ['API_PORT'].replace('tcp://','http://') + '/'
sklApi = SklItemApi(apiLocation)

while True:
	logging.info('Checking for new requests')
	items = sklApi.GetAllNew()

	logging.info('Found %s new requests',len(items))

	for item in items:
		process = sklApi.StartProcessing(item)
		fileLocation = generator.new(item)

		sklApi.CompleteProcessing(process)

		logging.info('Generated result for blah. Found at %s',fileLocation)

	logging.info("Sleeping for 10...")
	time.sleep(10)