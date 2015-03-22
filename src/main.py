from flask import Flask,send_file
from nap.url import Url
import urllib.request
import os
import generator
import logging
from SklItem import SklItem

app = Flask(__name__)
app.debug = True

logging.basicConfig(level=logging.DEBUG)

@app.route('/example')
def fractal_example():

	fileLocation = generator.generateExample()
	return send_file(fileLocation, mimetype='image/gif')

@app.route('/testapi')
def api_test():
	item = getItem()
	return item.resourceData

def getItem():
	apiLocation = os.environ['API_PORT']

	apiLocation = apiLocation.replace('tcp://','http://') + '/'

	logging.debug(apiLocation)

	api = Url(apiLocation) #API_PORT from docker

	# Get scenes
	scenes = api.get('scene').json()

	logging.debug(scenes)

	item = SklItem()

	item.resourceURL = scenes[0]['resource']['location']
	response = urllib.request.urlopen(item.resourceURL)
	item.resourceData = response.read().decode('utf-8')
	return item;

if __name__ == '__main__':
    app.run(host='0.0.0.0')