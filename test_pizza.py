import requests
from conftest import SITE

AUTH = {"Authorization": "token abcdef0123456789"}
VEGETARIAN = {"mustBeVegetarian": True}

# Vegetarian recommendations contain no non-vegetarian ingredients.
def test_vegetarian_pizza():
    res = requests.post(SITE + "/api/pizza", json=VEGETARIAN, headers=AUTH, timeout=15)
    assert res.status_code == 200
    body = res.json()
    assert body["pizza"]["name"]
    for ingredient in body["pizza"]["ingredients"]:
        assert ingredient["vegetarian"] is True, ingredient["name"]

# Recommendations without an authorization token are rejected.
def test_pizza_without_token_is_refused():
    res = requests.post(SITE + "/api/pizza", json=VEGETARIAN, timeout=15)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
