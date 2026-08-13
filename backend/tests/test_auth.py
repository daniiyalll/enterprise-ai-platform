def test_signup_requires_correct_secret_key(client):
    res = client.post("/api/v1/auth/signup", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "alicepass123",
        "role": "employee",
        "secret_key": "wrong-secret",
    })
    assert res.status_code == 403


def test_signup_and_login_success(client):
    signup_res = client.post("/api/v1/auth/signup", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "alicepass123",
        "role": "employee",
        "secret_key": "test-signup-secret",
    })
    assert signup_res.status_code == 200
    body = signup_res.json()
    assert body["username"] == "alice"
    assert body["role"] == "employee"

    login_res = client.post(
        "/api/v1/auth/login",
        data={"username": "alice", "password": "alicepass123"},
    )
    assert login_res.status_code == 200
    token = login_res.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_login_with_wrong_password_fails(client):
    client.post("/api/v1/auth/signup", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "bobpass123",
        "role": "employee",
        "secret_key": "test-signup-secret",
    })

    res = client.post(
        "/api/v1/auth/login",
        data={"username": "bob", "password": "wrong-password"},
    )
    assert res.status_code == 401


def test_duplicate_signup_fails(client):
    payload = {
        "username": "carol",
        "email": "carol@example.com",
        "password": "carolpass123",
        "role": "employee",
        "secret_key": "test-signup-secret",
    }
    first = client.post("/api/v1/auth/signup", json=payload)
    assert first.status_code == 200

    second = client.post("/api/v1/auth/signup", json=payload)
    assert second.status_code == 400
