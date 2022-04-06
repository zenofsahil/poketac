from pydantic import BaseModel
from typing import Optional

class PokemonInfo(BaseModel):
    name: str
    habitat: str
    description: Optional[str]
    isLegendary: bool

class PokemonInfoTranslated(BaseModel):
    name: str
