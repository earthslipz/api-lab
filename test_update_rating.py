import pytest

# Boundary values 0, 1, 5, 6: valid updates persist, rejected ones do not.
@pytest.mark.parametrize("stars,expected", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, expected):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected
    if expected == 200:
        assert res.json()["stars"] == stars
    else:
        assert "error" in res.json()
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json()["stars"] == (stars if expected == 200 else 3)
