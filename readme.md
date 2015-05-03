# Skeleton scene fractal generator

Part of the Skeleton Scene project, this generator is designed to create fractals.

## Using the generator

To build the docker image, assuming docker is setup, you can run:

    docker build -t mrjackdavis/skeleton-scene-generator-fractal .

When running the image, the environment variable `API_PORT` must be set to the url of the skeleton scene API. This can be done by using container linking, or by specifying the variable manually.

Specifying the url:

    -e "API_PORT=http://api.skeletonscene.com"

OR with container linking:

    --link skl-api:api

It's also necesary to set `S3_ACCESS_KEY` and `S3_SECRET_KEY`

    -e "S3_ACCESS_KEY=yourKey" -e "S3_SECRET_KEY=yourSecret"

#### Example

*Using container linking*

    docker run --name skl-fractal --link skl-api:api -e S3_ACCESS_KEY="yourKey" -e S3_SECRET_KEY="yourSecret" -d mrjackdavis/skeleton-scene-generator-fractal

Then, you can navigate to http://localhost:8080 and voila.

You can also mount `./src/` into the container so that it doesn't need to be re-run every time you make a change. You can do this by adding the following parameter:

    -v $(pwd)/src/:/app/