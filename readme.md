# Skeleton scene fractal generator

Part of the Skeleton Scene project, this generator is designed to create fractals.

## Using the generator

To build the docker image, assuming docker is setup, you can run:

    docker build -t mrjackdavis/skeleton-scene-generator-fractal .

When running the image, the environment variable `API_PORT` must be set to the url of the skeleton scene API. This can be done by using container linking, or by specifying the variable manually.

Specifying the url:

    docker run --name skl-fractal -p 8080:5000 -e "API_PORT=http://api.skeletonscene.com" -d mrjackdavis/skeleton-scene-generator-fractal

Container linking:

    docker run --name skl-fractal -p 8080:5000 --link skl-api:api -d mrjackdavis/skeleton-scene-generator-fractal

Then, you can navigate to http://localhost:8080 and voila.