import pytest

def func_with_arg(arg):
    return arg

def test_raise_exception():
    with pytest.raises(TypeError) as exc_info:
        func_with_arg()
    print(exc_info.value)