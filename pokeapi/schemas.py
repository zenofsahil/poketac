from pydantic import BaseModel
from typing import List, Optional

class PokemonInfo(BaseModel):
    name: str
