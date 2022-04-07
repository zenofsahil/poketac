import pytest
from pokeapi.client import requests
from pokeapi.main import pokemon_client
from datetime import datetime

class TestPokemonClient:
    def test_get_pokemon_info(self):
        raise NotImplementedError

    def test_get_pokemon_info_basic(self):
        raise NotImplementedError

    def test_get_pokemon_info_translated(self):
        raise NotImplementedError

    def test_fetch_url(self):
        """ The fetch_url method is trivially implemented and the core 
        caching functionality is already being tested in the 
        test_pokemonapi_client_caching test function.
        """
        assert True

    def test_translate_description(self):
        raise NotImplementedError

    def test_get_habitat(self):
        basic_info = {
            "name": "pikachu",
            "habitat": "forest",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": False
        }
        habitat = pokemon_client.get_habitat(basic_info)
        assert habitat == 'forest'

    def test_get_description(self, pokemon_data):
        pikachu_info = pokemon_data("pikachu")
        description = pokemon_client.get_description(pikachu_info)
        expected_description = "When several of these POKéMON gather, their electricity could build and cause lightning storms."
        assert description == expected_description

    def test_get_description_no_english_description_found(self, pokemon_data):
        pikachu_info = pokemon_data("pikachu")
        descriptions = [
            d for d in pikachu_info['flavor_text_entries']
            if d['language']['name'] != 'en'
        ]
        pikachu_info['flavor_text_entries'] = descriptions
        description = pokemon_client.get_description(pikachu_info)
        expected_description = None
        assert description == expected_description

    def test_translate_description(self):
        raise NotImplementedError

    def test_get_translation_kind_yoda_1(self):
        basic_info = {
            "name": "pikachu",
            "habitat": "forest",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": True
        }

        kind = pokemon_client.get_translation_kind(basic_info)
        assert kind == 'yoda'

    def test_get_translation_kind_yoda_2(self):
        basic_info = {
            "name": "pikachu",
            "habitat": "cave",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": False
        }

        kind = pokemon_client.get_translation_kind(basic_info)
        assert kind == 'yoda'

    def test_get_translation_kind_shakespeare_1(self):
        basic_info = {
            "name": "pikachu",
            "habitat": "forest",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": False
        }

        kind = pokemon_client.get_translation_kind(basic_info)
        assert kind == 'shakespeare'

    def test_pokemonapi_client_caching(monkeypatch):

        def patched(arg):
            return datetime.utcnow().timestamp()

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

