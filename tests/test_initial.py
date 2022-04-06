from fastapi.testclient import TestClient
from pokeapi.main import app

client = TestClient(app)

def test_pokemon_endpoint():
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]

def test_pokemon_translated_endpoint():
    response = client.get("/pokemon/translated/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]
