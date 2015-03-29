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
		fileLocation = generator.new(item)
		send_file(fileLocation, mimetype='image/gif')

	time.sleep(60)  # Delay for 1 minute (60 seconds)