import os
import time
import generator
import logging
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.connection import Location
from SklItemApi import SklItemApi
from ImageCompressor import compress

logging.basicConfig(level=logging.DEBUG)

# Get API URL from environment
apiLocation = os.environ['API_PORT'].replace('tcp://','http://') + '/'
sklApi = SklItemApi(apiLocation)
s3Connection = S3Connection(os.environ['S3_ACCESS_KEY'],os.environ['S3_SECRET_KEY'])

while True:
	logging.info('Checking for new requests')
	items = sklApi.GetAllNew()

	logging.info('Found %s new requests',len(items))

	for item in items:
		process = sklApi.StartProcessing(item)
		fileLocation = generator.new(process)
		logging.info("Finished generating %s:%s",item.id,process.id)

		if not fileLocation:
			raise Exception("File location was null")

		compressedFile = compress(fileLocation,50)

		logging.info("Uploading %s:%s (%s) to S3",item.id,process.id,compressedFile)
		
		bucket = s3Connection.get_bucket('skeleton-scene-app-web')
		k  = Key(bucket)
		k.key = 'generators/fractal/%s-%s.png' % (item.id,process.id)
		k.set_contents_from_filename(compressedFile)
		k.set_canned_acl('public-read')

		process.result="http://skeleton-scene-app-web.s3-website-ap-southeast-2.amazonaws.com/%s" % (k.key)

		sklApi.CompleteProcessing(process)

		logging.info('Generated result for %s:%s. Found at %s',item.id,process.id,process.result)


	logging.info("Sleeping for 10...")
	time.sleep(10)