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
        pass

    def test_translate_description(self):
        raise NotImplementedError

    def test_get_habitat(self):
        raise NotImplementedError


    def test_get_description(self):
        raise NotImplementedError

    def test_get_description_no_english_description_found(self):
        raise NotImplementedError

    def test_translate_description(self):
        raise NotImplementedError

    def test_get_translation_kind():
        raise NotImplementedError

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

