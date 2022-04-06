from typing import List, Optional
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from pokeapi import schemas

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pokemon/{pokemon_name}", response_model=List[schemas.PokemonInfo])
def get_pokemon_info(pokemon_name: str):
    pokemons = [
            { 'name': pokemon_name }
    ]
    return pokemons

@app.get("/pokemon/translated/{pokemon_name}", response_model=List[schemas.PokemonInfoTranslated])
def get_pokemon_info_translateed(pokemon_name: str):
    pokemons = [
            { 'name': pokemon_name }
    ]
    return pokemons

