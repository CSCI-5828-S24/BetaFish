import requests

BACKEND_URL = "https://betafish-flask-backend-3asud65paa-uc.a.run.app/"

def test_backend_is_deployed_and_healthy():
    response = requests.get(BACKEND_URL + "/api/health")
    assert response.status_code is 200