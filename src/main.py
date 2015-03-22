from flask import Flask,send_file
import os
import generator
import logging
from SklItemApi import SklItemApi

app = Flask(__name__)
app.debug = True

logging.basicConfig(level=logging.DEBUG)

# Get API URL from environment
apiLocation = os.environ['API_PORT'].replace('tcp://','http://') + '/'
sklApi = SklItemApi(apiLocation)

@app.route('/example')
def fractal_example():

	fileLocation = generator.generateExample()
	return send_file(fileLocation, mimetype='image/gif')

@app.route('/testapi')
def api_test():
	item = sklApi.GetOne()

	return item.resourceData

if __name__ == '__main__':
    app.run(host='0.0.0.0')