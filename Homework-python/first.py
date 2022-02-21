import pytest

def add5(v):
    myval = v + 5
    return myval

def tests_add5():
    r = add5(1)
    assert r == 6
    r = add5(5)
    assert r == 10
    r = add5(10.102645)
    assert r == 15.102645
