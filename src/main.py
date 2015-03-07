from flask import Flask,send_file
import generator
import logging

app = Flask(__name__)
app.debug = True

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def fractal_example():
	fileLocation = generator.generateExample()
	return send_file(fileLocation, mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0')