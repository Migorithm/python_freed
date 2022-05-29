from pytest import mark

def test_anything():
    assert 1==1

def test_something():
    assert 1 in [1,3,4]

@mark.xfail()
def test_string():
    assert 'fizz' not in 'fizzbuzz'