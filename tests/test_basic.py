# coding: utf-8
"""test_basic.py"""
import pytest


def test_math():
    assert 2 * 2 == 4


def test_bad_math():
    with pytest.raises(AssertionError):
        assert 2 ** 2 == 2
