# coding: utf-8
"""boardobject.py"""

from __future__ import print_function, unicode_literals

from simpletrello.trelloobject import TrelloObject

class Card(TrelloObject):

    def __init__(self, client, source_data=None):
        super(Card, self).__init__(client, source_data)
        self._populate_from_source(source_data)

    def _populate_from_source(self, source_data):
        self._id = source_data.get('id')
        self._name = source_data.get('name')
        self._closed = source_data.get('closed')
        self._desc = source_data.get('desc')
        self._id_board = source_data.get('idBoard')
        self._id_labels = source_data.get('idLabels')
        self._id_list = source_data.get('idList')
        self._id_members = source_data.get('idMembers')
        self._labels = source_data.get('labels')
        self._pos = source_data.get('pos')
        self._short_link = source_data.get('shortLink')
        self._subscribed = source_data.get('subscribed')
        self._full_data_cache = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        response = self.put(['cards', self.id], params={'name': value})
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
            raise ValueError('Card.closed expects a value of True or False')

    @property
    def comments(self):
        raise NotImplementedError('Comments are still on the simpletrello TODO list.')

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        response = self.put(['cards', self.id], params={'desc': value})
        if response['desc'] == value:
            self._desc = value

    @property
    def id_board(self):
        return self._id_board

    @property
    def id_list(self):
        return self._id_list

    @id_list.setter
    def id_list(self, value):
        self.move_to_list(value)

    @property
    def id_labels(self):
        return self._id_labels

    @property
    def id_members(self):
        raise NotImplementedError

    def add_comment(self, text):
        raise NotImplementedError

    def archive(self):
        response = self.put(['cards', self.id], params={'closed': 'true'})
        if response['closed'] == True:
            self._closed = True

    def unarchive(self):
        response = self.put(['cards', self.id], params={'closed': 'false'})
        if response['closed'] == False:
            self._closed = False

    def move_to_list(self, list_id):
        response = self.put(['cards', self.id], 
                params={'idList': list_id})
        if response['idList'] == list_id:
            self._id_list = list_id
            self.id_board = response['idBoard']