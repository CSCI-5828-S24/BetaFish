# run tests using pytest or python -m pytest
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
    response = client.get("/api/alldata?startTime=1713139200000&endTime=1713225600000&lat=39.74956044238265&long=-104.95078325271608&pageno=1&pagesize=20")
    assert response.status_code is 200

def test_crime_totals_endpoint_works_as_expected(client):
    response = client.get("/api/crime_totals")
    assert response.status_code is 200
