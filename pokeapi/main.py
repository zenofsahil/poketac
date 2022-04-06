from typing import List, Optional
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from pokeapi import schemas
from pokeapi.config import settings
from pokeapi import client

import logging
from pokeapi.config import settings

def get_log_level():
    if settings.LOG_LEVEL == 'INFO':
        return logging.INFO
    elif settings.LOG_LEVEL == 'DEBUG':
        return logging.DEBUG
    return logging.ERROR

logging.basicConfig(level=get_log_level())
logger = logging.getLogger(__name__)

logger.info('hello info')
logger.debug('hello debuug')

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pokemon_client = client.PokemonClient(
    base_url=settings.BASE_URL,
    endpoint=settings.ENDPOINT,
    translate_api=settings.TRANSLATE_API
)

@app.get("/pokemon/{pokemon_name}", response_model=List[schemas.PokemonInfo])
def get_pokemon_info(pokemon_name: str):
    pokemons = [
        pokemon_client.get_pokemon_info(name=pokemon_name, translate=False)
    ]
    return pokemons

@app.get("/pokemon/translated/{pokemon_name}", response_model=List[schemas.PokemonInfo])
def get_pokemon_info_translated(pokemon_name: str):
    pokemons = [
        pokemon_client.get_pokemon_info(name=pokemon_name, translate=True)
    ]
    return pokemons

