# coding: utf-8
"""test_client.py"""

import os
import pytest
from simpletrello import TrelloClient


def test_client():
    """Test that env variables are set and TrelloCLient instance is OK."""
    key = os.getenv('SIMPLETRELLO_API_KEY')
    token = os.getenv('SIMPLETRELLO_TOKEN')
    t = TrelloClient()
    assert isinstance(t, TrelloClient)
    assert repr(t) == '<simpletrello.TrelloCLient>(key={}...{}, token={}...{})'\
        .format(key[0], key[-1], token[0], token[-1])
