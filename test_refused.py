from conftest import log_in_new_user

# Registering a second account with an existing username is refused.
def test_duplicate_username_is_refused(api):
    import uuid
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}

# Logging in with a wrong password is refused.
def test_wrong_password_is_refused(api):
    import uuid
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users/token/login", json={**user, "password": "not-the-password"})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}

# Empty usernames are invalid.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
