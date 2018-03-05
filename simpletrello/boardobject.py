# coding: utf-8
"""boardobject.py"""

from __future__ import print_function, unicode_literals

from simpletrello.trelloobject import TrelloObject


class Board(TrelloObject):

    def __init__(self, client, source_data=None):
        super(Board, self).__init__(client, source_data)
        self._populate_from_source(self.source_data)

    def _populate_from_source(self, source_data):
        self._id = source_data.get('id')
        self._name = source_data.get('name')
        self._closed = source_data.get('closed', None)
        self._lists = None
        self._full_data_cache = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        response = self.put(['boards', self.id], params={'name': value})
        if response['name'] == value:
            self._name = value

    @property
    def closed(self):
        if self._closed is None:
            self.refresh_full_data()
        return self._closed

    @property
    def lists(self):
        if not self._lists:
            self.refresh_lists()
        return self._lists

    @property
    def cards(self):
        return self.client.get_cards_by_board(self._id)

    @property
    def full_data(self):
        if not self._full_data_cache:
            self.refresh_full_data()
        return self._full_data_cache

    def refresh_lists(self):
        self._lists = self.client.get_board_lists(self.id)

    def refresh_full_data(self):
        self._full_data_cache = self.client.get_board(self.id, fields='all', raw=True)
        self._populate_from_source(self._full_data_cache)

    def create_list(self, list_name, pos='bottom'):
        new_list = self.client.create_list(
            list_name=list_name,
            id_board=self.id,
            pos=pos
        )
        self.refresh_lists()
        return new_list

    def archive(self):
        response = self.put(['boards', self.id], params={'closed': 'true'})
        if response['closed'] is True:
            self._closed = True

    def unarchive(self):
        response = self.put(['boards', self.id], params={'closed': 'false'})
        if response['closed'] is False:
            self._closed = False

    def delete(self):
        """Delete the board.
        WARNING: Deletion is irreversible.
        Consider archiving instead.
        """
        response = self.client.delete_board(self.id)
        if response['_value'] is None:
            # TODO
            pass

    def rename(self, new_name):
        response = self.put(['boards', self.id], params={'name': new_name})
        if response['name'] == new_name:
            self.name = new_name

    def __repr__(self):
        return('<simpletrello.boardobject.Board ({}, {})>'.format(self.name, self.id))
