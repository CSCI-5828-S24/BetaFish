from datetime import datetime
import time
import requests
from dateutil.relativedelta import relativedelta

BACKEND_URL = "https://betafish-flask-backend-3asud65paa-uc.a.run.app"
COLLECTOR_URL = "https://us-central1-csci-5828-final-project.cloudfunctions.net/betafish-collector"
ANALYZER_URL = "https://us-central1-csci-5828-final-project.cloudfunctions.net/betafish-analyzer"

def test_backend_is_deployed_and_healthy():
    response = requests.get(BACKEND_URL + "/api/health")
    assert response.status_code == 200

def test_backend_is_not_storing_beyond_31_days():
    timeToFilter = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=33)
    startReportedDateFilter = int(time.mktime(timeToFilter.timetuple()) * 1000)
    timeToFilter = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=32)
    endReportedDateFilter = int(time.mktime(timeToFilter.timetuple()) * 1000)
    response = requests.get(BACKEND_URL + f"/api/alldata?startTime={startReportedDateFilter}&endTime={endReportedDateFilter}&lat=39.74956044238265&long=-104.95078325271608&pageno=1&pagesize=20")
    assert len(response.json()['data']) == 0
    assert response.status_code == 200

# premise: there will always be at least one crime each day
def test_backend_is_storing_for_last_31_days():
    timeToFilter = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=31)
    startReportedDateFilter = int(time.mktime(timeToFilter.timetuple()) * 1000)
    timeToFilter = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=30)
    endReportedDateFilter = int(time.mktime(timeToFilter.timetuple()) * 1000)
    response = requests.get(BACKEND_URL + f"/api/alldata?startTime={startReportedDateFilter}&endTime={endReportedDateFilter}&lat=39.74956044238265&long=-104.95078325271608&pageno=1&pagesize=20")
    assert len(response.json()['data']) > 0
    assert response.status_code == 200


def test_collector_prod():
    response = requests.get(COLLECTOR_URL)
    assert response.text == "done!!"
    assert response.status_code == 200


def test_analyzer_prod():
    response = requests.get(ANALYZER_URL)
    assert response.text == "success"
    assert response.status_code == 200
