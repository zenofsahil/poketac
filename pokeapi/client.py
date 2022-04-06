import requests
from typing import Optional
from urllib.parse import urljoin

class PokemonClient:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def get_pokemon_info(self, name: str) -> dict:
        """
        Get basic information for the pokemon as specified by `name`
        """
        url = urljoin(self.base_url, f'{self.endpoint}/{name}')
        r = requests.get(url)

        if r.ok and r.json() is not None:
            response = {
                'name' : r.json().get('name', name),
                'description' : self.get_description(r.json()),
                'habitat' : self.get_habitat(r.json()),
                'isLegendary' : r.json().get('is_legendary', False)
            }
            return response
        else:
            raise Exception

    @staticmethod
    def get_habitat(json_content: dict) -> Optional[str]:
        """
        Extract the habitat value from the `json_content`
        """
        habitat = json_content.get('habitat')
        return habitat.get('name') if habitat else None
            
    @staticmethod
    def get_description(json_content: dict) -> Optional[str]:
        """
        Extract the printable english description from the `json_content`
        """
        descriptions = json_content.get('flavour_text_entries')

        if descriptions is not None and len(descriptions) > 0:
            for description in descriptions:
                language = description.get('language')
                if (
                    language is not None and
                    language.get('name') is not None and
                    language.get('name') == 'en' and
                    description.get('flavor_text') is not None
                ):
                    return description.get('flavor_text')
        return None

