import pytest
from cards import Card
"""
The code looks pretty much the same as it did before, 
with the exception of some extra white space and each method has to have an initial self argument.
We can now run all of these together by specifying the class:

$ cd /path/to/code/ch2
$ pytest -v TDD/05_classes_test.py::TestEquality

"""

class TestEquality:
    def test_equality(self):
        c1 = Card("something", "brian", "todo", 123) 
        c2 = Card("something", "brian", "todo", 123) 
        assert c1 == c2
    def test_equality_with_diff_ids(self):
        c1 = Card("something", "brian", "todo", 123) 
        c2 = Card("something", "brian", "todo", 4567) 
        assert c1 == c2
    def test_inequality(self):
        c1 = Card("something", "brian", "todo", 123)
        c2 = Card("completely different", "okken", "done", 123) 
        assert c1 != c2
