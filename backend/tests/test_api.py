def test_health_returns_ok(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_is_empty_at_first(client):
    response = client.get("/api/applications")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_returns_201_and_the_new_row(client):
    response = client.post(
        "/api/applications",
        json={"company": "Google", "role": "SWE Intern"},
    )
    assert response.status_code == 201

    body = response.get_json()
    assert body["company"] == "Google"
    # the database filled these in for us
    assert body["status"] == "applied"
    assert body["id"] > 0


def test_created_row_shows_up_in_the_list(client, sample):
    body = client.get("/api/applications").get_json()
    assert len(body) == 1
    assert body[0]["company"] == "Stripe"


def test_create_without_role_is_rejected(client):
    response = client.post("/api/applications", json={"company": "Google"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_blank_company_is_rejected(client):
    # whitespace only should count as empty
    response = client.post(
        "/api/applications",
        json={"company": "   ", "role": "SWE Intern"},
    )
    assert response.status_code == 400


def test_patch_changes_only_the_fields_sent(client, sample):
    response = client.patch(
        f"/api/applications/{sample['id']}",
        json={"status": "offer"},
    )
    assert response.status_code == 200

    body = response.get_json()
    assert body["status"] == "offer"
    # the role was not in the request, so it should be untouched
    assert body["role"] == "Backend Intern"


def test_patch_on_a_missing_id_is_404(client):
    response = client.patch("/api/applications/999", json={"status": "offer"})
    assert response.status_code == 404


def test_patch_ignores_columns_that_are_not_allowed(client, sample):
    # id is not in the allowed list, so this should be rejected
    response = client.patch(f"/api/applications/{sample['id']}", json={"id": 42})
    assert response.status_code == 400


def test_delete_removes_the_row(client, sample):
    response = client.delete(f"/api/applications/{sample['id']}")
    assert response.status_code == 204

    # the list should be empty again
    assert client.get("/api/applications").get_json() == []


def test_delete_on_a_missing_id_is_404(client):
    response = client.delete("/api/applications/999")
    assert response.status_code == 404
