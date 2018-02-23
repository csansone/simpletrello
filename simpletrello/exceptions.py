# coding: utf-8
"""exceptions.py"""

from __future__ import print_function, unicode_literals


class RateLimitExceeded(Exception):
    """Raise when an http request returns status code 429.
    There is a limit of 300 requests per 10 seconds for each API key
    and no more than 100 requests per 10 second interval for each token.
    If a request exceeds the limit, Trello will return a 429 error.
    """
    pass


class AuthenticationError(Exception):
    """Raise when expected API credentials are not found."""
    pass
