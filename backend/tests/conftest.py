import os
import sys

import pytest

# let the tests import app.py and db.py from the folder above
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app
from db import init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    # tmp_path is a fresh empty folder pytest makes for each test
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    init_db()

    flask_app.config["TESTING"] = True
    # the test client sends requests without starting a real server
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def sample(client):
    # one application already in the database, for tests that need it
    response = client.post(
        "/api/applications",
        json={"company": "Stripe", "role": "Backend Intern"},
    )
    return response.get_json()
