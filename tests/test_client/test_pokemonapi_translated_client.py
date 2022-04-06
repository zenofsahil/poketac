def test_pokemonapitranslated_client(client):
    response = client.get("/pokemon/translated/pikachu")
    assert response.status_code == 200
    assert response.json() == [{"name": "pikachu"}]
