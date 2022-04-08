import pytest
from unittest.mock import Mock
from requests.models import Response
from pokeapi.client import requests
from pokeapi.main import create_translate_client
from datetime import datetime

@pytest.fixture(name="translate_client")
def translate_client():
    return create_translate_client()

class TestTranslateClient:
    def test_extract_translation(self, translate_client):
        response = {
            "success": {
                "total": 1
            },
            "contents": {
                "translated": "At which hour several of these pokémon gather,  their electricity couldst buildeth and cause lightning storms.",
                "text": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
                "translation": "shakespeare"
            }
        }
        translation =  "At which hour several of these pokémon gather,  their electricity couldst buildeth and cause lightning storms."

        assert translate_client.extract_translation(response) == translation


    def test_translate_description(self, monkeypatch, translate_client):
        """
        This test is there only to test the end to end functionality of the
        `translate_description` method.
        """
        basic_info = {
            "name": "pikachu",
            "habitat": "forest",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": True
        }

        def patched(arg):
            res = Mock(spec=Response)
            res.json.return_value = {
                "success": {
                    "total": 1
                },
                "contents": {
                    "translated": "At which hour several of these pokémon gather,  their electricity couldst buildeth and cause lightning storms.",
                    "text": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
                    "translation": "shakespeare"
                }
            }
            res.status_code = 200
            return res
        
        monkeypatch.setattr(requests, 'get', patched)

        expected_output = {
            "name": "pikachu",
            "habitat": "forest",
            "description": "At which hour several of these pokémon gather,  their electricity couldst buildeth and cause lightning storms.",
            "isLegendary": True
        }


        translated_res = translate_client.translate_description(basic_info)
        assert translated_res == expected_output

    def test_get_translation_kind_yoda_1(self, translate_client):
        basic_info = {
            "name": "pikachu",
            "habitat": "forest",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": True
        }

        kind = translate_client.get_translation_kind(basic_info)
        assert kind == 'yoda'

    def test_get_translation_kind_yoda_2(self, translate_client):
        basic_info = {
            "name": "pikachu",
            "habitat": "cave",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": False
        }

        kind = translate_client.get_translation_kind(basic_info)
        assert kind == 'yoda'

    def test_get_translation_kind_shakespeare(self, translate_client):
        basic_info = {
            "name": "pikachu",
            "habitat": "forest",
            "description": "When several of these POKéMON gather, their electricity could build and cause lightning storms.",
            "isLegendary": False
        }

        kind = translate_client.get_translation_kind(basic_info)
        assert kind == 'shakespeare'

    def test_translate_client_caching(self, monkeypatch, translate_client):
        """ Duplicate of pokemon client test
        """

        def patched(arg):
            res = Mock(spec=Response)
            res.json.return_value = datetime.utcnow().timestamp()
            res.status_code = 200
            return res

        monkeypatch.setattr(requests, 'get', patched)
        data1 = translate_client.fetch_url('https://sample.url')
        # The return value for 'https://sample.url' has now been cached. So if we
        # were to call it again, it should be the same as when we first called it.
        data2 = translate_client.fetch_url('https://sample.url')

        # The value for 'https://another.url' has not been cached and will be newly
        # computed.
        data3 = translate_client.fetch_url('https://another.url')

        assert data1 == data2
        assert data1 != data3
        assert data2 != data3

