import pytest
import time

@pytest.fixture(scope="module") 
def data():
    time.sleep(1)
    return 3


def test_data_one(data):
    assert data*3 ==9 

def test_data_two(data):
    assert data*3 ==9 

def test_data_three(data):
    assert data*3 ==9 

def test_data_sample(data_sample):
    assert data_sample==1

def test_data_to_give(data_to_give):
    assert data_to_give == 3