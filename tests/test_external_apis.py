import pytest

def test_pokemon_api_sample_response_1():
    raise NotImplementedError

def test_pokemon_api_sample_response_2():
    raise NotImplementedError

def test_pokemon_api_incorrect_pokemon_query():
    raise NotImplementedError

@pytest.mark.xfail(strict=False, reason="Rate limited API. 5 calls per hour.")
def test_translation_api_shakespeare_translation_1():
    """ WARNING: This is an expensive test.
    """
    raise NotImplementedError

@pytest.mark.xfail(strict=False, reason="Rate limited API. 5 calls per hour.")
def test_translation_api_yoda_translation_1():
    """ WARNING: This is an expensive test.
    """
    raise NotImplementedError

def test_translation_api_shakespeare_incorrect_query():
    raise NotImplementedError

