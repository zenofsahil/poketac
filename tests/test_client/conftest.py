import pytest
from fastapi.testclient import TestClient
from pokeapi.main import app


@pytest.fixture(name='client')
def test_client():
    return TestClient(app)
