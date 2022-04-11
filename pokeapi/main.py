import logging
from datetime import datetime, timedelta

from fastapi import status
from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from pokeapi import schemas
from pokeapi.config import settings
from pokeapi import client
from pokeapi.exceptions import (
    PokemonAPIException,
    PokemonAPIHTTPException,
    TranslationAPIException,
    TranslationAPIHTTPException
)
from pokeapi.redis import redis_client

def get_log_level():
    if settings.LOG_LEVEL == 'INFO':
        return logging.INFO
    elif settings.LOG_LEVEL == 'DEBUG':
        return logging.DEBUG
    return logging.ERROR

logging.basicConfig(level=get_log_level())
logger = logging.getLogger(__name__)

def create_app():
    app = FastAPI(title=settings.PROJECT_NAME)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

async def rate_limit_middleware(request: Request, call_next):
    logger.info(f"Received request from: {request.client.host}")

    # Do not rate limit development or testing environment
    if settings.ENVIRONMENT == "test":
        return await call_next(request)

    if redis_client.get(request.client.host) is None:
        redis_client.set(
            request.client.host, 1, ex=timedelta(seconds=settings.RATE_LIMIT_SECONDS)
        )
    else:
        hitcount = redis_client.get(request.client.host)
        hitcount = int(hitcount)

        logger.debug(f"Host: {request.client.host} has hitcount: {hitcount} within rate limit time window.")

        if hitcount >= settings.RATE_LIMIT_HITS:
            logger.debug("Rate limit exceeded by {request.client.host}")
            return PlainTextResponse("Rate limit exceeded", status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            redis_client.set(request.client.host, hitcount + 1, keepttl=True)

    return await call_next(request)

app = create_app()
app.middleware('http')(rate_limit_middleware)

def create_pokemon_client():
    return client.PokemonClient(
        base_url=settings.BASE_URL,
        endpoint=settings.ENDPOINT
    )

def create_translate_client():
    return client.TranslateClient(
        translate_url=settings.TRANSLATE_API
    )

@app.get("/pokemon/{pokemon_name}", response_model=schemas.PokemonInfo)
def get_pokemon_info(pokemon_name: str, pokemon_client = Depends(create_pokemon_client)):

    try:
        pokemon = pokemon_client.get_pokemon_info(name=pokemon_name)
    except PokemonAPIHTTPException:
        # Resurface http exceptions to be handled by their own handler
        raise
    except:
        raise PokemonAPIException

    return pokemon

@app.get("/pokemon/translated/{pokemon_name}", response_model=schemas.PokemonInfo)
def get_pokemon_info_translated(
    pokemon_name: str,
    pokemon_client = Depends(create_pokemon_client),
    translate_client = Depends(create_translate_client)
):
    try:
        pokemon = pokemon_client.get_pokemon_info(name=pokemon_name)
    except PokemonAPIHTTPException:
        # Resurface http exceptions to be handled by their own handler
        raise 
    except: 
        raise PokemonAPIException

    try:
        translated = translate_client.translate_description(pokemon)
    except TranslationAPIHTTPException:
        # Resurface http exceptions to be handled by their own handler
        raise
    except:
        raise TranslationAPIException

    return translated

