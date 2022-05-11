import pytest
import pytest
from app.calculations import add, subtract, multiply, divide

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (1, 1, 2)
])
def test_add(num1, num2, expected):
    print("HIII")
    #sum = add(5,3)
    #assert False #if given true value assert True, if false assert False
    #assert add(5,3) == 8
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(5,3) == 2

def test_multiply():
    assert multiply(5,3) == 15

def test_divide():
    assert divide(6,3) == 2