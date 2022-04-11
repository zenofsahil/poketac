import logging
from fastapi import status
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
async def pokemon_api_http_exception_handler(request: Request, exc: PokemonAPIHTTPException):
    logger.error(exc.detail)
    return PlainTextResponse(exc.detail, status_code=exc.status_code)

@app.exception_handler(TranslationAPIHTTPException)
async def pokemon_translation_api_http__exception_handler(request: Request, exc: TranslationAPIHTTPException):
    logger.error(exc.detail)
    return PlainTextResponse(exc.detail, status_code=exc.status_code)

@app.exception_handler(TranslationAPIException)
async def pokemon_translation_api_exception_handler(request: Request, exc: TranslationAPIException):
    logger.error(f"{exc.__class__.__name__}")
    return PlainTextResponse("Internal Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.exception_handler(PokemonAPIException)
async def pokemon_api_exception_handler(request: Request, exc: PokemonAPIException):
    logger.error(f"{exc.__class__.__name__}")
    return PlainTextResponse("Internal Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
