# coding: utf-8
"""listobject.py"""

from __future__ import print_function, unicode_literals

from simpletrello.trelloobject import TrelloObject


class List(TrelloObject):
    def __init__(self, client, source_data=None, with_cards=False):
        super(List, self).__init__(client, source_data=None)
        self._populate_from_source(source_data=source_data, with_cards=with_cards)

    def _populate_from_source(self, source_data, with_cards):
        self._id = source_data.get('id')
        self._id_board = source_data.get('idBoard')
        self._name = source_data.get('name')
        self._pos = source_data.get('pos')
        self._subscribed = source_data.get('subscribed')
        self._closed = source_data.get('closed')
        self._cards = None
        if with_cards:
            self._get_cards()

    @property
    def id(self):
        return self._id

    @property
    def id_board(self):
        return self._id_board

    @id_board.setter
    def id_board(self, value):
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        response = self.put(['lists', self.id], params={'name': value})
        if response['name'] == value:
            self._name = value

    @property
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        if value in [True, 'true']:
            self.archive()
        elif value in [False, 'false']:
            self.unarchive()
        else:
            raise ValueError('List.closed expects a value of True or False')

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        raise NotImplementedError

    @property
    def cards(self):
        if not self._cards:
            self._get_cards()
        return self._cards

    @property
    def subscribed(self):
        if self._subscribed is not None:
            return self._subscribed
        self.refresh_full_data()
        return self._subscribed

    def refresh_full_data(self):
        self._full_data_cache = self.client.get_list(self.id, fields='all', raw=True)
        self._populate_from_source(self._full_data_cache)

    def create_card(
            self,
            card_name,
            desc=None,
            pos='bottom'):
        response = self.client.create_card(card_name, self.id)
        return response

    def _get_cards(self):
        self._cards = self.client.get_cards(list_id=self.id)

    def move_list_to(self, id_board, pos='bottom'):
        pass

    def copy_list_to(self, id_board, pos='bottom'):
        new_list = self.client.create_list(self.name, id_board, pos, self.id)
        return new_list

    def __repr__(self):
        return('<simpletrello.listobject.List ({}, {})>'.format(self.name, self.id))
