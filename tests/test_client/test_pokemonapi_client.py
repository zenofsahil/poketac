def test_pokemonapi_client(client):
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]
