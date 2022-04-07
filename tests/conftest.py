import pytest
import json
from fastapi.testclient import TestClient
from pokeapi.main import app

@pytest.fixture(name='client')
def test_client():
    return TestClient(app)

@pytest.fixture(name="pokemon_data")
def pokemon_data():
    def extract_data(name):
        assert name in ["crobat", "ditto", "heatran", "pikachu"]
        f = open(f"tests/test_data/pokeapi_responses/{name}.json", 'r').read()
        data = json.loads(f)
        return data
    return extract_data
