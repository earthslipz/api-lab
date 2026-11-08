import requests
from conftest import SITE

AUTH = {"Authorization": "token abcdef0123456789"}

# A read-only public token can list the available cutting tools.
def test_tools_are_listed():
    res = requests.get(SITE + "/api/tools", headers=AUTH, timeout=15)
    assert res.status_code == 200
    assert res.json() == {"tools": ["Knife", "Pizza cutter", "Scissors"]}
