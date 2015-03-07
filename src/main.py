from flask import Flask,send_file
import generator

app = Flask(__name__)
app.debug = True


@app.route('/')
def fractal_example():
	fileLocation = generator.generateExample()
	return send_file(fileLocation, mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0')