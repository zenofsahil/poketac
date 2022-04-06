import requests
from typing import Optional
from urllib.parse import urljoin

class PokemonClient:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def get_pokemon_info(self, name):
        return { 'name': name }

    def _get_pokemon_info(self, name):
        url = urljoin(self.base_url, f'{self.endpoint}/{name}')
        print(url)
        r = requests.get(url)
        return r
    @staticmethod
    def get_description(self, json_content: dict) -> Optional[str]:
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


class PokemonTranslatedClient:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def get_pokemon_info(self, name):
        return { 'name': name }


