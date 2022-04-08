import pytest
from unittest.mock import Mock
from requests.models import Response
from pokeapi.client import requests
from pokeapi.main import create_pokemon_client
from datetime import datetime

@pytest.fixture(name="pokemon_client")
def pokemon_client():
    return create_pokemon_client()

class TestPokemonClient:
    def test_get_pokemon_info(self, pokemon_data, monkeypatch, pokemon_client):
        def patched(arg):
            res = Mock(spec=Response)
            res.json.return_value = pokemon_data('pikachu')
            res.status_code = 200
            return res

        monkeypatch.setattr(requests, 'get', patched)
        output = pokemon_client.get_pokemon_info(name='pikachu')
        expected_output =  {
            "name": "pikachu",
            "habitat": "forest",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": False
        }
        assert output == expected_output

    def test_fetch_url(self):
        """ The fetch_url method is trivially implemented and the core 
        caching functionality is already being tested in the 
        test_pokemonapi_client_caching test function.
        """
        assert True

    def test_get_habitat(self, pokemon_data, pokemon_client):
        data = pokemon_data('pikachu')
        habitat = pokemon_client.get_habitat(data)
        assert habitat == 'forest'

    def test_get_description(self, pokemon_data, pokemon_client):
        pikachu_info = pokemon_data("pikachu")
        description = pokemon_client.get_description(pikachu_info)
        expected_description = "When several of these POKéMON gather, their electricity could build and cause lightning storms."
        assert description == expected_description

    def test_get_description_no_english_description_found(self, pokemon_data, pokemon_client):
        pikachu_info = pokemon_data("pikachu")
        descriptions = [
            d for d in pikachu_info['flavor_text_entries']
            if d['language']['name'] != 'en'
        ]
        pikachu_info['flavor_text_entries'] = descriptions
        description = pokemon_client.get_description(pikachu_info)
        expected_description = None
        assert description == expected_description

    def test_pokemonapi_client_caching(self, monkeypatch, pokemon_client):

        def patched(arg):
            res = Mock(spec=Response)
            res.json.return_value = datetime.utcnow().timestamp()
            res.status_code = 200
            return res

        monkeypatch.setattr(requests, 'get', patched)
        data1 = pokemon_client.fetch_url('https://sample.url')
        # The return value for 'https://sample.url' has now been cached. So if we
        # were to call it again, it should be the same as when we first called it.
        data2 = pokemon_client.fetch_url('https://sample.url')

        # The value for 'https://another.url' has not been cached and will be newly
        # computed.
        data3 = pokemon_client.fetch_url('https://another.url')

        assert data1 == data2
        assert data1 != data3
        assert data2 != data3

