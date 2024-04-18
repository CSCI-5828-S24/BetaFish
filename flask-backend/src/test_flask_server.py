# run tests using pytest or python -m pytest
import os
import tempfile
import pytest

from flask_server import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING" : True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_health_endpoint_works_as_expected(client):
    response = client.get("/api/health")
    assert response.status_code is 200

def test_all_data_endpoint_works_as_expected(client):
    response = client.get("/api/alldata")
    assert response.status_code is 200
