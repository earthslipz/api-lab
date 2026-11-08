# A second user cannot read the owner's private rating.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    own = api.get(path, headers=auth)
    assert own.status_code == 200
    assert own.json()["stars"] == 3

# A second user cannot change the owner's stars.
def test_other_user_cannot_update(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 5}, headers=other_auth)
    assert 400 <= res.status_code <= 499
    own = api.get(path, headers=auth)
    assert own.status_code == 200
    assert own.json()["stars"] == 3

# A second user cannot delete the owner's rating.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    own = api.get(path, headers=auth)
    assert own.status_code == 200
    assert own.json()["stars"] == 3
