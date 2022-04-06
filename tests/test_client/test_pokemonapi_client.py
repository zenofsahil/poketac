import pytest
from pokeapi.client import requests
from pokeapi.main import pokemon_client
from datetime import datetime

def test_payload_keys(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200

    payload = response.json()[0]

    assert "name" in payload
    assert "description" in payload
    assert "habitat" in payload
    assert "isLegendary" in payload


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


@pytest.mark.skip(reason="Should belong in integration tests")
def test_pokemonapi_client(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]
