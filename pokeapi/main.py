import logging
from typing import List, Optional
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from pokeapi import schemas
from pokeapi.config import settings
from pokeapi import client
from pokeapi.exceptions import (
    PokemonAPIException,
    PokemonAPIHTTPException,
    TranslationAPIException,
    TranslationAPIHTTPException
)

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

app = create_app()

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
        raise 
    except: 
        raise PokemonAPIException

    try:
        translated = translate_client.translate_description(pokemon)
    except TranslationAPIHTTPException:
        raise
    except:
        raise TranslationAPIException

    return translated

