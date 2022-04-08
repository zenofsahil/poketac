from pydantic import BaseModel
from typing import Optional

class PokemonInfo(BaseModel):
    name: str
    habitat: Optional[str]
    description: Optional[str]
    isLegendary: bool

