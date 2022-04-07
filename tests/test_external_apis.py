import os
import pytest
import requests
from urllib.parse import urljoin
from requests.models import PreparedRequest

def test_pokemon_api_sample_response():
    """
    The pokeapi response should carry at least the following keys for our
    API to work correctly.

    - name
    - habitat
    - flavor_text_entries
    - is_legendary
    """
    base_url = os.environ.get('BASE_URL', 'https://pokeapi.co')
    endpoint = os.environ.get('ENDPOINT', 'api/v2/pokemon-species')
    pokemon_name = 'pikachu'
    url = urljoin(base_url, f'{endpoint}/{pokemon_name}')
    r = requests.get(url)

    assert r.ok 
    assert r.json() is not None

    json = r.json()

    assert 'name' in json
    assert 'habitat' in json
    assert 'flavor_text_entries' in json
    assert 'is_legendary' in json
    
@pytest.mark.skip()
@pytest.mark.xfail(strict=False, reason="Rate limited API. 5 calls per hour.")
def test_translation_api_shakespeare_translation():
    """ WARNING: This is an expensive test.
    """
    text = "What will be, will be."

    translate_api = os.environ.get('TRANSLATE_API', 'https://api.funtranslations.com/translate')
    translation_url = urljoin(translate_api, f'translate/yoda')
    request_data = {'text': text}

    prepared_request = PreparedRequest()
    prepared_request.prepare_url(translation_url, request_data)

    r = requests.get(prepared_request.url)

    assert r.ok
    assert r.json() is not None

    json = r.json()

    
    from IPython import embed 
    from traitlets.config import get_config 
    c = get_config() 
    c.InteractiveShellEmbed.colors = "Linux" 
    embed(config=c)
     

    assert 'success' in json
    assert 'contents' in json

