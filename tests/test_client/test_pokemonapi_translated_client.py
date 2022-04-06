def test_payload_keys(client):
    response = client.get("/pokemon/translated/pikachu")
    assert response.status_code == 200

    payload = response.json()[0]

    assert "name" in payload
    assert "description" in payload
    assert "habitat" in payload
    assert "isLegendary" in payload
