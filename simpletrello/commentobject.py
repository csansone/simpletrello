# coding: utf-8
"""commentobject.py"""

from __future__ import print_function, unicode_literals

from simpletrello.trelloobject import TrelloObject


class Comment(TrelloObject):

    def __init__(self, client, source_data=None):
        super(Comment, self).__init__(client, source_data)
        self.populate_from_source(source_data)

    def populate_from_source(self, source_data):
        _data = source_data.get('data')
        self._id = source_data.get('id')
        self._id_board = _data.get('board', {}).get('id')
        self._id_member_creator = source_data.get('idMemberCreator')
        self._id_card = _data.get('card', {}).get('id')
        self._id_list = _data.get('list', {}).get('id')
        self._text = _data.get('text')
        self._date = source_data.get('date')

    @property
    def id(self):
        return self._id

    @property
    def id_board(self):
        return self._id_board

    @property
    def id_card(self):
        return self._id_card

    @property
    def id_member_creator(self):
        return self._id_creator

    @property
    def id_list(self):
        return self._id_list

    @property
    def date(self):
        return self._date

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        """Edit comment text, then refresh entire comment.
        Main reasoning for full refresh is to keep correct date."""
        params = {'text': value}
        response = self.put(['actions', self.id], params=params)
        if response['data']['text'] == value:
            # self._text = value
            self.populate_from_source(response)

    def __repr__(self):
        if len(self.text) > 10:
            repr_text = '{}...'.format(self.text[:10])
        else:
            repr_text = self.text
        return('<simpletrello.commentobject.Comment ({}, {})>'.format(repr_text, self.id))
