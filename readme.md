# Skeleton scene fractal generator

Part of the Skeleton Scene project, this generator is designed to create fractals.

## Using the generator

To build the docker image, assuming docker is setup, you can run:

    docker build -t mrjackdavis/skeleton-scene-generator-fractal .

Then to run the afformentioned image in a container, run the following:

    docker rm -f skl-fractal && docker run --name skl-fractal -p 8080:5000 -d mrjackdavis/skeleton-scene-generator-fractal

Then, you can navigate to http://localhost:8080 and voila.