import pytest

@pytest.fixture()
def simple_data():
    return 42

def test_fixture(simple_data):
    assert simple_data==42