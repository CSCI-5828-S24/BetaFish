from main import analyze

def test_analyzer_success():
    assert analyze(None) == 'success'