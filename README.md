Poketac
===

This is a proof of concept app that uses [pokeapi](https://pokeapi.co) and [funtranslations](https://funtranslations.com/) to provide users with two endpoints:

1. `/pokemon/<name>`
2. `/pokemon/translated/<name>`

The endpoints provide basic information about the pokemon specified. The `translated` endpoint will provide a quirky translation by yoda or shakespeare :)


Running
-------

Your system will need to have Docker available. Once you ensure you have Docker, clone this repo using 
```
$ git clone git@github.com:zenofsahil/poketac.git
```

Check the environment variables as defined inside `sample.envars` and rename the file to `.envars`. It needs to stay within the project root.

The application is defined entirely within the docker related files. You can check those out to see what's happening under the
hood. But the project setup and running is as easy as the following -

These commands should be performed inside the project root directory.

Spin up the containers with
```
$ docker-compose up -d --build
```

Stop and remove containers with
```
$ docker-compose down
```

Using the API
-------------

Poketac is built with [FastAPI](https://fastapi.tiangolo.com/) so OpenAPI specifications are provided out of the box. You can visit `localhost:8000/docs` to see the schemas and use the API inside your browser. You can also get the OpenAPI schema from `localhost:8000/openapi.json`. 

To use the API from the terminal with curl, 
```
$ curl -i localhost:8000/pokemon/pikachu

$ curl -i localhost:8000/pokemon/translated/pikachu`
```

Please note that the application implements rate limiting based on the host that is making the query. The rate limiting window and the number of hits permitted within that window are defined within the `.envars` settings file.

Running Tests
-------

Test with
```
$ docker-compose run pokeapi bash -c "ENVIRONMENT=test python -m pytest -v"
```

You need to set the `ENVIRONMENT` environment variable to make the application not rate limit while running tests.

Application features
------------
1. Robust unit test suite
2. Logging
3. Rate limiting
    - You can control rate limiting by setting the `RATE_LIMIT_HITS` and `RATE_LIMIT_SECONDS` environment variables in the `.envars` file. These variables control how many times (`RATE_LIMIT_HITS`) per (`RATE_LIMIT_SECONDS`) seconds users of the api can make requests.

Good to haves
------------
1. Sentry
2. CI/CD
3. Auth using tokens
4. Test coverage metrics
5. Integration test suite
   - The unit test suit is present and covers most functionality. It would also be good to have integrations tests for things such as rate limiting in the context of the live application.
6. Load testing metrics
7. Caching API responses in Redis
    - Currently the application uses in-memory caching for requests (explained in the code) requests caching should be brought to the caching layer built on redis. Redis is already being used for rate limiting functionality.
8. Type checking using **mypy**
9. Application usage reports using **Celery**
10. Trimmed down `requirements.txt` file. Contains a lot of development related requirements.

License
-------
MIT
