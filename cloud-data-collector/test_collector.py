# run tests using pytest or python -m pytest
from main import collect

def test_collector():
    assert collect(None) == "done!!"