from calculator import square
import pytest

def test_positive():
    assert square(2, 2) == 4
    assert square(3, 0) == 1

def test_negative():
    assert square(-2, 2) == 4
    assert square(-3, 3) == -27

def test_zero():
    assert square(0, 2) == 0

def test_str():
    with pytest.raises(TypeError):
        square("cat", "cat")