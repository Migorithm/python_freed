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

### Parametrization
We’ll look at three ways to implement parametrized testing in pytest in the order in which they should be selected:
- Parametrizing functions
- Parametrizing fixtures
- Using a hook function called **"pytest_generate_tests"**

```python
from dataclasses import dataclass,asdict

@dataclass
class User:
    id :str
    age:int
    name:str

def test_finish(): 
    for u in [
        User("saka1023",20,"Migo"),
        User("saka1024",25,"Mago"),
        User("saka1025",32,"Mego"),    
    ]:
        assert u.name.startswith("M")

```
```sh
$ pytest test_finish_combined.py
========================= test session starts ========================== collected 1 item
test_finish_combined.py . [100%]
========================== 1 passed in 0.01s ===========================
```
It passes but there are some problems:
- We have one test case reported instead of three.
- If one of the test cases fails, we really don’t know which one without looking at the traceback or some other debugging information
- If one of the test cases fails, the test cases following the failure will not be run. pytest stops running a test when an assert fails.

#### Parametrizing Functions
To parametrize a test function, add parameters to the test definition and use the **@pytest.mark.parametrize()** decorator to define the sets of arguments to pass to the test, like this:
```python
@pytest.mark.parametrize(
    "IDs,Ages,Names",
    [
        ("saka1023",20,"MIGO"),
        ("zaka1023",24,"Zigo"),
        ("eaka123",93,"Tigo"),
    ],
)
def test_fenish(IDs,Ages,Names):
    initial_user=User(id=IDs,age=Ages,name=Names)
    assert initial_user.age >= 20

```
The first argument to @pytest.mark.parametrize() is a list of names of the parameters.<br>
They are strings and can be an actual list of strings, as in ["start_summary", "start_state"], or<br>
they can be a comma-separated string, as in "start_summary, start_state".<br><br>

The second argument to @pytest.mark.parametrize() is our list of test cases.

#### Parametrizing fixtures
```python
@pytest.fixture(params=[5,6,7])
def parameters(request):
    return request.param

def test_params(parameters):
    assert parameters>=5
```

```sh
TDD/09_parametrization_test.py::test_params[5] PASSED                                                                               [ 71%]
TDD/09_parametrization_test.py::test_params[6] PASSED                                                                               [ 85%]
TDD/09_parametrization_test.py::test_params[7] PASSED                                                                               [100%]
```
What happens is pytest ends up calling parameters() three times, once each for all values in params.<br>
Each value of **params** is saved to **request.param** for the fixture to use. 


### Configuration files
Configuration files—those non-test files that affect how pytest runs—save time and duplicated work.<br>
- **pytest.ini** : This is the primary pytest configuration file that allows you to change pytest's default behaviour. Its location also defines the pytest root directory, or rootdir.
- **conftest.py** : This file contains fixtures and hook functions. It can exist at the rootdir or in any subdirectory.
- \_\_init\_\_.py : When put into test subdirectories, this file allows you to have identical test file names in multiple test directories<br><br>


PROJECT<br>
├── ... top level project files, src dir, docs, etc ...<br>
├── pytest.ini<br>
└── tests<br>
  ├── conftest.py <br>
  ├── api<br>
  │ ├── \_\_init\_\_.py<br>
  │ ├── conftest.py<br>
  │ └── ... test files for api ...<br>
  └── cli<br>
    ├── __init__.py<br>
    ├── conftest.py<br>
    └── ... test files for cli ...<br>

#### Saving Settings and Flags in pytest.ini
Let's take a look at an example **pytest.ini** file.
```ini
[pytest]
addopts = 
  --strict-markers
  --strict-config
  -ra
  -v 

testpaths = tests
markers =
  smoke: subset of tests
  exception: check for expected expcetions
```
Explanation: <br>
The addopts setting enables us to list the pytest flags we always want to run in this project.<br>
The testpaths setting tells pytest where to look for tests if you haven’t given a file or directory name on the command line.<br>


#### Avoiding Test File Name Collision
The \_\_init\_\_.py file affects pytest in one way and one way only: it allows you to have duplicate test file names.<br>
If you have \_\_init\_\_.py files in every test subdirectory, you can have the same test file name show up in multiple directories.<br>
That’s it—the only reason to have a \_\_init\_\_.py file. Here is an example:<br>
tests_with_init<br>
├── api<br>
│ ├── \_\_init\_\_.py<br>
│ └── test_add.py<br>
├── cli<br>
│ ├── \_\_init\_\_.py<br>
│ └── test_add.py<br>
└── pytest.ini<br>

```sh
$ pytest -v tests_with_init
========================= test session starts ========================== collected 2 items
tests_with_init/api/test_add.py::test_add PASSED [ 50%] tests_with_init/cli/test_add.py::test_add PASSED [100%]
========================== 2 passed in 0.02s ===========================
```



