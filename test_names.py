import requests
from conftest import SITE

# The public names endpoint returns a list including Margherita.
def test_names_are_listed():
    res = requests.get(SITE + "/api/names", timeout=15)
    assert res.status_code == 200
    assert "Margherita" in res.json()["names"]
