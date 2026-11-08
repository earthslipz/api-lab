# Creating a rating returns its id, stars and pizza id.
def test_create_rating(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 5}, headers=auth)
    assert res.status_code == 201
    body = res.json()
    assert body["stars"] == 5
    assert body["pizza_id"] == pizza_id
    assert isinstance(body["id"], int)

# The owner can retrieve the rating just created.
def test_read_rating(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating

# The owner can update the rating's stars.
def test_update_rating(api, auth, rating):
    res = api.put(f"/api/ratings/{rating['id']}", json={"stars": 4}, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == 4

# A deleted rating cannot be retrieved again.
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    assert api.delete(path, headers=auth).status_code == 204
    assert api.get(path, headers=auth).status_code == 404
