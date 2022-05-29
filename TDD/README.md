### Running pytest
To run pytest, you have the option to specify files and directories.<br>
If not specified, pytest will look for tests in the current working directory and subdir.<br>
It looks for .py files that are either:<br>
- *starting with test_* or 
- *ending with _test*



### Option
- -v: for verbosity 
```sh
pytest -v test_script.py
```

- --tb=no : No tracebacks
```sh
pytest --tb=no
```


### Test discoverity
Given no arguments, pytest looks at your current directory and all subdirectories for test files<br>
and runs the test code it finds.<br>
If you give pytest a filename or directory name, or a list of those, it looks there instead of the current directory.<br><br>
Brief overview of the naming conventions to keep your test code discoverble by pytest:
- Test files should be named **test_{something}.py** or **{something}_test.py**
- Test methods and functions should be named **test_{something}**
- Test classes should be named **Test{Somthing}** (Camel Case)


### Test Outcomes
Here are the possible outcomes of a test:
- PASSED (.)—The test ran successfully. 
- FAILED (F)—The test did not run successfully.
- SKIPPED (s)—The test was skipped. You can tell pytest to skip a test by using the following decorators: 
    - @pytest.mark.skip() 
    - @pytest.mark.skipif() 

- XFAIL (x)—The test was **not supposed to pass**, and it ran and failed. You can tell pytest that a test is expected to fail by using:
    - @pytest.mark.xfail() decorator
   
- XPASS (X)—The test was marked with xfail, but it ran and passed.
- ERROR (E)—An exception happened either during the execution of a fixture or hook function, and not during the execution of a test function.

### Using assert statement
When you write test functions, the normal Python assert statement is your primary tool to communicate test failure.

**pytest                      unittest**
assert something            assertTrue(something)
assert not something        assertFalse(something)
assert a == b               assertEqual(a, b)
assert a != b               assertNotEqual(a, b)
assert a is None            assertIsNone(a)
assert a is not None        assertIsNotNone(a) 
assert a <= b ......        assertLessEqual(a, b)


### Testing for Expected Exceptions
You use pytest.raises() to test for expected exceptions.
```python
import pytest
def CardsDB(argument):
    print(argument)

def test_no_path_raises(): 
    with pytest.raises(TypeError):
        CardsDB()

```


### Structuring Test Functions
I recommend making sure you keep assertions at the end of test functions.<br>
It has at least two names: Arrange-Act-Assert and Given-When-Then.<br>
Regardless of the names of the steps, the goal is the same: separate a test into stages.<br>
```python
def test_to_dict():
    # GIVEN a Card object with known contents
    c1 = Card("something", "brian", "todo", 123) 

    # WHEN we call to_dict() on the object
    c2 = c1.to_dict()

    # THEN the result will be a dictionary with known content
    c2_expected = { 
        "summary": "something", 
        "owner": "brian", "state": "todo",
        "id": 123,
            }
    assert c2 == c2_expected

```
- **Given/Arrange** — A starting state. This is where you set up data or the environment to get ready for the action.
- **When/Act** — Some action is performed. This is the focus of the test—the behavior we are trying to make sure is working right.
- **Then/Assert** — Some expected result or end state should happen. At the end of the test, we make sure the action resulted in the expected behavior.


### Running a Subset of Tests
Subset                                        Syntax
Single test method                            pytest path/test_module.py::TestClass::test_method
All tests in a class                          pytest path/test_module.py::TestClass
Single test function                          pytest path/test_module.py::test_function
All tests in a module                         pytest path/test_module.py
All tests in a directory                      pytest path
Tests matching a name pattern                 pytest -k pattern

```sh
#Let’s run all the tests with “equality” in their name:
pytest -v --tb=no -k equality

#we can eliminate certain pattern by expanding the expression:
$ pytest -v --tb=no -k "equality and not equality_fail"
```

### fixtures
Fixtures are functions that are run by pytest before (and sometimes after) the actual test functions. 
```python
import pytest

@pytest.fixture() 
def some_data():
    """Return answer to ultimate question."""
    return 42
def test_some_data(some_data):
    """Use fixture return value in a test.""" 
    assert some_data == 42
```

```sh
% pytest -v TDD/06_fixture_get_started_test.py
...
...
collected 1 item                                                                                                   

TDD/06_fixture_get_started_test.py::test_fixture PASSED                                                      [100%]
================================================ 1 passed in 0.00s 
```

### Using Fixtures for Setup and Teardown

```python
from pathlib import Path
from tempfile import TemporaryDirectory 
import cards
import pytest

@pytest.fixture() 
def cards_db():
    with TemporaryDirectory() as db_dir: 
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path) 
        yield db
        db.close()

def test_empty(cards_db): 
    assert cards_db.count() == 0
```

The cards_db fixture is “setting up” for the test by getting the database ready. It’s then yield-ing the database object.<br><br>

Fixture functions run before the tests that use them. If there is a yield in the function, it stops there, passes control to the tests.<br><br>

The code above the yield is “setup” and the code after yield is “teardown.”<br><br>

The teardown, is guaranteed to run regardless of what happens during the tests.

### Specifying Fixture Scope

Each fixture has a specific scope, which defines the order of when the setup and teardown run relative to running of all the test function using the fixture.<br>
The default scope for fixtures is function scope.<br>
<br>
HOWEVER, there may be times when you don’t want that to happen.<br>
Perhaps setting up and connecting to the database is time-consuming,<br>
or you are generating large sets of data, or you are retrieving data from a server or a slow device. <br>
Let’s change the scope of our fixture so the database is only opened once, and then talk about different scopes.

```python
import pytest

@pytest.fixture(scope="module") 
def cards_db():
    with TemporaryDirectory() as db_dir: 
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db 
        db.close()
```
The fixture decorator scope parameter allows more than function and module.<br>
There’s also **class**, **package**, and **session**. The default scope is function.<br><br>


### Sharing Fixtures through conftest.py
You can put fixtures into individual test files, but to share fixtures among multiple test files, you need to use a **conftest.py** file either in the same directory as the test file that’s using it or in some parent directory.<br>

#### Finding Where Fixtures Are Defined
```
$ pytest --fixtures -v
```
Adding -v will include the entire docstring.<br>
You can also use --fixtures-per-test to see what fixtures are used by each test and where the fixtures are defined:


### Using Multiple Fixture Levels
Say two tests suite depend on the database being empty to start with, If they insert some data into DB and
close it, the second test being called will not have empty DB. But still, we want to try to stick with one open database.

```python
import pytest

@pytest.fixture(scope="session") 
def db():
    """CardsDB object connected to a temporary database"""
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db_ = cards.CardsDB(db_path) yield db_
        db_.close()
@pytest.fixture(scope="function") 
def cards_db(db):
    """CardsDB object that's empty"""
    db.delete_all() 
    return db
```

### Using Multiple Fixtures per Test or Fixture
conftest.py:
```python
@pytest.fixture(scope="session") 
def some_cards():
    """List of different Card objects"""
    return [
    cards.Card("write book", "Brian", "done"), 
    cards.Card("edit book", "Katie", "done"), 
    cards.Card("write 2nd edition", "Brian", "todo"), 
    cards.Card("edit 2nd edition", "Katie", "todo"),
    ]

@pytest.fixture(scope="function") 
def cards_db(db):
    """CardsDB object that's empty"""
    db.delete_all() 
    return db
```

Then we can use both empty_db and some_cards in a test:
```python
def test_add_some(cards_db, some_cards): 
    expected_count = len(some_cards)
    for c in some_cards:
        cards_db.add_card(c)
    assert cards_db.count() == expected_count
```


### Deciding Fixture Scope Dynamically
We can do dynamically decide the scope of the db fixture at runtime. 
First, we change the scope of db:<br>
conftest.py:
```python
@pytest.fixture(scope=db_scope) ##  
def db():
    """CardsDB object connected to a temporary database"""
    with TemporaryDirectory() as db_dir: 
        db_path = Path(db_dir)
        db_ = cards.CardsDB(db_path) yield db_
        db_.close()

def db_scope(fixture_name, config):
    if config.getoption("--func-db", None):
    return "function" return "session"
```
There are many ways we could have figured out which scope to use, but in this case, I chose to depend on a new command-line flag, **--func-db**. In order to allow pytest to allow us to use this new flag, we need to write a **hook function**.<br>

```python
def pytest_addoption(parser): 
    parser.addoption(
        "--func-db", 
        action="store_true", 
        default=False,
        help="new db for each test",
    )
```