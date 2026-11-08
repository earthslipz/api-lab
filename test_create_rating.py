import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"

# Base choice: integer 3 stars, an existing pizza and a valid user token.
def test_base_choice_is_saved(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id

# C1: Values outside 1..5 are invalid.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": stars}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}

# C2: Fractional stars are not whole numbers.
def test_decimal_stars_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3.5}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()

# C2: A string cannot replace an integer rating.
def test_text_stars_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": "3"}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()

# C2: A missing stars field is rejected.
def test_missing_stars_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()

# C3: A nonexistent pizza cannot be rated.
def test_unknown_pizza_refused(api, auth):
    res = api.post("/api/ratings", json={"pizza_id": 999999999, "stars": 3}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()

# C4: Missing authorization is refused.
def test_missing_token_refused(api, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}

# C4: A short invalid token is refused.
def test_short_token_refused(api, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers={"Authorization": "token short"})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
