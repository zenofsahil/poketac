import pytest

def test_payload_keys(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200

    payload = response.json()[0]

    assert "name" in payload
    assert "description" in payload
    assert "habitat" in payload
    assert "isLegendary" in payload

def test_payload_keys_translation_endpoint(client):
    response = client.get("/pokemon/translated/pikachu")
    assert response.status_code == 200

    payload = response.json()[0]

    assert "name" in payload
    assert "description" in payload
    assert "habitat" in payload
    assert "isLegendary" in payload

def test_valid_request():
    """
    Test for /pokemon/pikachu
    """
    raise NotImplementedError

def test_invalid_pokemon():
    """
    Test for /pokemon/spiderman
    """
    raise NotImplementedError

def test_pokemon_api_down():
    raise NotImplementedError

def test_translation_api_down():
    raise NotImplementedError

@pytest.mark.parametrize('endpoint', range(5))
def test_incorrect_endpoint_hit(endpoint):
    raise NotImplementedError

@pytest.mark.skip(reason="Should belong in integration tests")
def test_pokemonapi_client(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]
