import pytest

@pytest.mark.parametrize('pokemon_name', [
    'pikachu',
    'charizard',
    'snorlax',
    'heatran',
    'ditto',
    'mew',
    'mewtwo',
    'dialga',
    'lopunny',
    'gible'
])
def test_payload_keys(client, pokemon_name):
    response = client.get(f"/pokemon/{pokemon_name}")
    assert response.status_code == 200

    payload = response.json()

    assert "name" in payload
    assert "description" in payload
    assert "habitat" in payload
    assert "isLegendary" in payload

@pytest.mark.skip(reason="Expensive Test. Rate limited API")
def test_payload_keys_translation_endpoint(client):
    response = client.get("/pokemon/translated/pikachu")
    assert response.status_code == 200

    payload = response.json()

    assert "name" in payload
    assert "description" in payload
    assert "habitat" in payload
    assert "isLegendary" in payload

def test_valid_pokemon(client):
    """
    Test for /pokemon/pikachu
    """
    r = client.get("/pokemon/pikachu")

    assert r.ok 
    assert r.json() is not None

def test_invalid_pokemon(client):
    """
    Test for /pokemon/spiderman
    """
    r = client.get("/pokemon/spiderman")

    assert r.ok == False
    assert r.status_code == 404

@pytest.mark.parametrize('url_part', [
    "/pokemons/hello",
    "/index.html",
    "/admin",
    "/pokemon/pikachu/hello",
    "/pokemon/translate/",
    "/pokemon/translate/pikachus?q=hello"
])
def test_incorrect_endpoint_hit(url_part, client):
    response = client.get(url_part)
    assert response.status_code == 404

@pytest.mark.skip(reason="Should belong in integration tests")
def test_pokemonapi_client(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]
