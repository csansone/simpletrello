"""labelobject.py"""

from __future__ import print_function, unicode_literals

from simpletrello.trelloobject import TrelloObject


class Label(TrelloObject):

    def __init__(self, client, source_data=None):
        super(Label, self).__init__(client, source_data)
        self._populate_from_source(self.source_data)

    def _populate_from_source(self, source_data):
        self._id = source_data.get('id')
        self._id_board = source_data.get('idBoard')
        self._name = source_data.get('name')
        self._color = source_data.get('color')

    @property
    def id(self):
        return self._id

    @property
    def id_board(self):
        return self._id_board

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        response = self.put(['labels', self.id], params={'name': value})
        if response['name'] == value:
            self._name = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        response = self.put(['labels', self.id], params={'color': value})
        if response['color'] == value:
            self._color = value

    def __repr__(self):
        name = self.name if len(self.name) > 0 else '<unnamed>'
        return('<simpletrello.labelobject.Label ({}, {}, {})>'.format(name, self.color, self.id))
