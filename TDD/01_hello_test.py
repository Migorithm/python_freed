from pytest import mark

def test_sample():
    assert 1 ==1

@mark.xfail()
def test_failing():
    assert (1,2,3) == (6,2,4)


"""
How to? 
- pytest script.py
- pytest -v script.py (For verbosity)

"""