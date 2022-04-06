import pytest

def test_payload_keys(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200

    payload = response.json()[0]

    assert "name" in payload
    assert "description" in payload
    assert "habitat" in payload
    assert "isLegendary" in payload


@pytest.mark.skip(reason="Should belong in integration tests")
def test_pokemonapi_client(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]
