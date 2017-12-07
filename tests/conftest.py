# coding: utf-8
"""conftest.py"""

import time
import pytest
from simpletrello import TrelloClient

@pytest.fixture(scope='session')
def client():
	"""Client instance to be used for all tests.
	The following two environment variables must be set:
	
	SIMPLETRELLO_API_KEY
	SIMPLETRELLO_TOKEN
	"""
	return TrelloClient()

@pytest.fixture(scope='session')
def testid():
	"""Create a 'unique enough' number for naming of test objects."""
	t = time.time()
	seconds, partial = str(t).split('.')
	testid = ''.join((seconds[-5:], partial[:3]))
	return testid

@pytest.fixture(scope='session')
def board_id_existing():
	return '59b20aa457b03ce5735de812'