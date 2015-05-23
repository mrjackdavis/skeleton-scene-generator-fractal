import os
import time
import generator
import logging
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.connection import Location
from SklItemApi import SklItemApi
from ImageCompressor import compress
from ImageCompressor import compressAndScale

logging.basicConfig(level=logging.DEBUG)

# Get API URL from environment
apiLocation = os.environ['API_PORT'].replace('tcp://','http://') + '/v0-2/'
sklApi = SklItemApi(apiLocation)
s3Connection = S3Connection(os.environ['S3_ACCESS_KEY'],os.environ['S3_SECRET_KEY'])

def uploadItemToS3(pathToImg,itemID):
	logging.info("Uploading %s (%s) to S3",itemID,pathToImg)

	bucket = s3Connection.get_bucket('skeleton-scene-app-web')
	k  = Key(bucket)
	k.key = 'generators/fractal/%s.png' % (itemID)
	k.set_contents_from_filename(pathToImg)
	k.set_canned_acl('public-read')

	return "http://skeleton-scene-app-web.s3-website-ap-southeast-2.amazonaws.com/%s" % (k.key)


while True:
	logging.info('Checking for new requests')
	items = sklApi.GetAllNew()

	logging.info('Found %s new requests',len(items))

	for item in items:
		sklApi.StartProcessing(item)
		fileLocation = generator.new(item)
		logging.info("Finished generating %s",item.id)

		if not fileLocation:
			raise Exception("File location was null")

		resultFullSizeFilePath = compress(fileLocation,80)
		resultThumbnailFilePath = compressAndScale(fileLocation,50,120)

		item.resultURL=uploadItemToS3(resultFullSizeFilePath,item.id)
		item.thumbnailURL=uploadItemToS3(resultThumbnailFilePath,item.id)

		sklApi.CompleteProcessing(item)

		logging.info('Generated result for %s. Found at %s',item.id,item.resultURL)


	logging.info("Sleeping for 10...")
	time.sleep(10)