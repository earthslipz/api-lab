import pytest

# Returned pizza must not use any excluded tool (0, 1 or 2 exclusions).
@pytest.mark.parametrize("excluded", [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]])
def test_excluded_tool_is_not_used(api, auth, excluded):
    res = api.post("/api/pizza", json={"excludedTools": excluded}, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded

# Excluding all three tools should be a client error, not a server crash.
@pytest.mark.xfail(reason="Defect 1: excluding every tool returns HTTP 500 with an empty body instead of JSON 400", strict=True)
def test_all_tools_excluded_returns_clear_error(api, auth):
    res = api.post("/api/pizza", json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}, headers=auth)
    assert res.status_code == 400
    assert res.headers.get("Content-Type", "").startswith("application/json")
    assert isinstance(res.json().get("error"), str)
    assert res.json()["error"]
