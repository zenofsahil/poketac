import logging
from fastapi import Request
from fastapi.responses import PlainTextResponse
from pokeapi.main import app
from pokeapi.exceptions import (
    PokeAPIException,
    PokemonAPIException,
    PokemonAPIHTTPException,
    TranslationAPIException,
    TranslationAPIHTTPException
)

logger = logging.getLogger(__name__)
    
@app.exception_handler(PokemonAPIHTTPException)
async def pokemon_exception_handler(request: Request, exc: PokemonAPIHTTPException):
    logger.error(exc.detail)
    return PlainTextResponse(exc.detail, status_code=exc.status_code)

@app.exception_handler(TranslationAPIHTTPException)
async def pokemon_exception_handler(request: Request, exc: TranslationAPIHTTPException):
    logger.error(exc.detail)
    return PlainTextResponse(exc.detail, status_code=exc.status_code)
