# run tests using pytest or python -m pytest
import os
import tempfile
import pytest

from flask_server import create_app
import jsonpickle

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

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code is 200