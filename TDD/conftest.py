import pytest

@pytest.fixture(scope='module')
def data_sample():
    return 1

def data_scope(fixture_name, config):
    if config.getoption("--func-db", None):
        return "function" 
    return "session"

@pytest.fixture(scope=data_scope)
def data_to_give():
    return 3

def pytest_addoption(parser): 
    parser.addoption(
        "--func-db", 
        action="store_true", 
        default=False,
        help="new db for each test",
        )

@pytest.fixture(params=[5,6,7])
def parameters(request):
    return request.param