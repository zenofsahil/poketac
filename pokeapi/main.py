from typing import List, Optional
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

import schemas

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=List[schemas.PokemonInfo])
def get_pokemon_info():
    pokemons = [
            { 'name': 'charizard' }, { 'name': 'pikachu' }
    ]
    return pokemons


