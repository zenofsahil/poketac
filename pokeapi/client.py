import requests
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

class PokemonTranslatedClient:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def get_pokemon_info(self, name):
        return { 'name': name }


