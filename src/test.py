import os
import time
import generator
import logging
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.connection import Location
from SklItem import SklItem
from SklProcess import SklProcess

logging.basicConfig(level=logging.DEBUG)



logging.info('Running test')

item = SklItem('test',time.time(),'http://www.google.com')
process = SklProcess(time.time(),item,"InProgress")

fileLocation = generator.new(process)
logging.info("Finished generating %s",item.id)

if not fileLocation:
	raise Exception("File location was null")

logging.info('Generated result for %s. Found at %s',item.id,fileLocation)