def signup_and_login(client, username, role, secret="test-signup-secret"):
    client.post("/api/v1/auth/signup", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "somepassword123",
        "role": role,
        "secret_key": secret,
    })
    res = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": "somepassword123"},
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_employee_cannot_create_workflow(client):
    headers = signup_and_login(client, "emp1", "employee")
    res = client.post(
        "/api/v1/workflows/",
        json={"name": "Test WF", "description": "desc"},
        headers=headers,
    )
    assert res.status_code == 403


def test_manager_can_create_and_list_workflows(client):
    headers = signup_and_login(client, "mgr1", "manager")

    create_res = client.post(
        "/api/v1/workflows/",
        json={"name": "Onboarding", "description": "New hire onboarding"},
        headers=headers,
    )
    assert create_res.status_code == 200
    body = create_res.json()
    assert body["name"] == "Onboarding"
    assert body["is_active"] is True

    list_res = client.get("/api/v1/workflows/", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1


def test_only_admin_can_delete_workflow(client):
    manager_headers = signup_and_login(client, "mgr2", "manager")
    create_res = client.post(
        "/api/v1/workflows/",
        json={"name": "Expense Approval", "description": "desc"},
        headers=manager_headers,
    )
    workflow_id = create_res.json()["id"]

    denied = client.delete(f"/api/v1/workflows/{workflow_id}", headers=manager_headers)
    assert denied.status_code == 403

    admin_headers = signup_and_login(client, "admin1", "admin")
    allowed = client.delete(f"/api/v1/workflows/{workflow_id}", headers=admin_headers)
    assert allowed.status_code == 200


def test_workflows_require_authentication(client):
    res = client.get("/api/v1/workflows/")
    assert res.status_code in (401, 403)
