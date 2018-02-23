# coding: utf-8
"""trelloobject.py"""

from __future__ import print_function, unicode_literals


class TrelloObject(object):
    """Parent class for the other objects.

    Objects that inherit from TrelloObject include:

    - boardobject.Board
    - cardobject.Card
    - commentobject.Card
    - listobject.List
    """
    def __init__(self, client, source_data=None):
        self.client = client
        self.source_data = source_data

    def get(self, *args, **kwargs):
        return self.client._get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.client._post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.client._put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.client._delete(*args, **kwargs)

    def print_summary(self):
        """Print common attributes to console."""
        attributes_to_print = ['id', 'name', 'date',
            'desc', 'url', 'closed']

        for attr in attributes_to_print:
            try:
                print('{}: {}'.format(attr, getattr(self, attr)))
            except AttributeError:
                pass

    def __repr__(self):
        """Nobody should ever see this, as TrelloObject is expected
        to always be subclassed as Board, List, or Card.
        """
        return('<TrelloObject, yo> {}'.format(self.id))
