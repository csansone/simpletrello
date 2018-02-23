# coding: utf-8
"""client.py"""

from __future__ import print_function, unicode_literals

import logging
import os
import requests

from simpletrello.boardobject import Board
from simpletrello.cardobject import Card
from simpletrello.commentobject import Comment
from simpletrello.exceptions import AuthenticationError, RateLimitExceeded
from simpletrello.listobject import List
from simpletrello.utils import listify, combine_values, is_stringy

API_VERSION = '1'
TRELLO_URL = 'https://api.trello.com/{}'.format(API_VERSION)
logger = logging.getLogger(__name__)


class TrelloClient():

    def __init__(self, api_key=None, token=None):
        self.set_credentials(api_key=api_key, token=token)

    def set_credentials(self, api_key, token):
        if api_key is not None:
            self._api_key = api_key
        else:
            try:
                self._api_key = os.environ['SIMPLETRELLO_API_KEY']
            except KeyError:
                raise AuthenticationError('No api_key param or SIMPLETRELLO_API_KEY found.')
        if token is not None:
            self._token = token
        else:
            try:
                self._token = os.environ['SIMPLETRELLO_TOKEN']
            except KeyError:
                raise AuthenticationError('No token param or SIMPLETRELLO_TOKEN found.')

    def define_url(self, path_parts):
        path_parts = listify(path_parts)
        path_parts.insert(0, TRELLO_URL)
        url = '/'.join(path_parts)
        return url

    ### HTTP METHODS ###

    def _http_request(
            self,
            method,
            path_parts,
            as_json=True,
            params=None):
        """Make http request to Trello API.

        Params
        ------
        method: str
            one of 'get' | 'post' | 'put' | 'delete'

        path_parts: list

        as_json: bool

        Returns
        -------
        response: JSON by default
            if as_json == False, returns a <requests.models.Response> object.
        """
        if not params:
            params = {}
        else:
            assert isinstance(params, dict)
        url = self.define_url(path_parts)
        payload = {'key': self._api_key, 'token': self._token}
        payload.update(params)
        if method == 'get':
            response = requests.get(url, params=payload)
        elif method == 'post':
            response = requests.post(url, params=payload)
        elif method == 'put':
            response = requests.put(url, params=payload)
        elif method == 'delete':
            response = requests.delete(url, params=payload)

        # Check for response errors before returning anything
        if response.ok is False:
            if response.status_code == 429:
                # Trello API returns 429 for rate limit exceeded.
                raise RateLimitExceeded
            # All other status errors
            log_text = 'Status code {}: {} on URL {}'.format(
                response.status_code, response.text, response.url)
            logger.error(log_text)
            response.raise_for_status()

        if as_json is True:
            _json = response.json()
            return _json
        else:
            return response

    def _get(self, path_parts, as_json=True, params=None):
        """Perform a GET request against Trello API."""
        response = self._http_request(
            method='get',
            path_parts=path_parts,
            as_json=as_json,
            params=params)
        return response

    def _post(self, path_parts, as_json=True, params=None):
        response = self._http_request(
            method='post',
            path_parts=path_parts,
            as_json=as_json,
            params=params)
        return response

    def _put(self, path_parts, as_json=True, params=None):
        """Perform a PUT request against Trello API."""
        response = self._http_request(
            method='put',
            path_parts=path_parts,
            as_json=as_json,
            params=params)
        return response

    def _delete(self, path_parts, as_json=True, params=None):
        """Perform a DELETE request against Trello API."""
        response = self._http_request(
            method='delete',
            path_parts=path_parts,
            as_json=as_json,
            params=params)
        assert response['_value'] is None
        return response

    def get_all_boards(self):
        """Return a list of Board objects."""
        response = self._get(['members', 'me', 'boards'], as_json=True)
        boards = []
        for board_json in response:
            boards.append(Board(self, board_json))
        return boards

    def get_board_by_name(self, board_name, partial=False):
        """Return a single board instance. Expect exactly one board to have <board_name>.
        If no boards or multiple boards have <board_name>, raise an exception.
        Case insensitive.
        """
        boards = self.search_boards_by_name(board_name)
        matches = []
        for board in boards:
            if board.name.lower().strip() == board_name.lower().strip():
                matches.append(board)
        if len(matches) == 0:
            raise ValueError('No boards with matching name.')
        if len(matches) > 1:
            raise ValueError('More than one board matches searched name.')
        return matches[0]

    def search_boards_by_name(self, name_to_search):
        result = self.search(name_to_search, model_types='boards')
        boards = [Board(self, info) for info in result['boards']]
        return boards

    def get_board(self, board_id, fields=None, raw=False):
        # if fields:
        #     params = {'fields': combine_values(fields)}
        params = {'fields': combine_values(fields)} if fields else None
        response = self._get(['boards', board_id], params=params)
        if raw:
            # Return a dict of data as returned by API
            return response
        board = Board(self, source_data=response)
        return board

    def get_board_lists(self, board_id, with_cards=False):
        """Return a list of <List>s from <board_id>.
        Each <List> is an instance of listobject.List
        """
        response = self._get(['board', board_id, 'lists'], params={'fields': 'all'})
        board_lists = [List(self, source_data=list_source, with_cards=with_cards)
                       for list_source in response]
        return board_lists

    def get_list(self, list_id, fields='all', raw=False):
        params = {'fields': combine_values(fields)} if fields else None
        response = self._get(['lists', list_id], params=params)

        if raw:
            # Return a dict of data as returned by API
            return response
        return List(self, source_data=response)

    def get_card(self, card_id):
        response = self._get(['cards', card_id])
        return Card(self, source_data=response)

    def get_cards(self, board_id=None, list_id=None):
        if board_id:
            if list_id:
                raise ValueError('Pass only one of board_id or list_id')
            response = self._get(['boards', board_id, 'cards'])
        elif list_id:
            response = self._get(['lists', list_id, 'cards'])
        else:
            raise ValueError('Pass either board_id or list_id.')
        cards = [Card(self, card_source) for card_source in response]
        return cards

    def get_cards_by_board(self, board_id):
        response = self._get(['boards', board_id, 'cards'])
        return [Card(self, card_source) for card_source in response]

    def get_card_comments(self, card_id):
        params = {'filter': 'commentCard'}
        response = self._get(['cards', card_id, 'actions'], params=params)
        return [Comment(self, comment_source) for comment_source in response]

    def get_comment_by_id(self, comment_id):
        response = self._get(['actions', comment_id])
        return Comment(self, response)

    ### CREATE NEW ITEMS

    def create_board(self, params=None):
        if is_stringy(params):
            # Allow for a single string to be passed in , and use it as the board name.
            params = {'name': params}
        response = self._post(['boards'], params=params)
        new_board = Board(self, response)
        return new_board

    def create_list(self, list_name, id_board, pos='bottom', list_id_to_copy=None):
        params = {
            'name': list_name,
            'idBoard': id_board,
            'pos': pos,
        }
        if list_id_to_copy:
            params['idListSource'] = list_id_to_copy
        response = self._post(['lists'], params=params)
        new_list = List(self, response)
        return new_list

    def create_card(self, card_name, id_list, desc=None, pos='bottom', card_id_to_copy=None):
        params = {
            'name': card_name,
            'idList': id_list,
            'desc': desc,
            'pos': pos,
        }
        if card_id_to_copy:
            params['idCardSource'] = card_id_to_copy
        response = self._post(['cards'], params=params)
        new_card = Card(self, response)
        return new_card

    ### DELETE ITEMS

    def delete_board(self, board_id):
        """Delete board identified by board_id.

        This does delete the board, but it needs work.
        """
        response = self._delete(['boards', board_id])
        assert response['_value'] is None
        return response

    ### SEARCH

    def search(self, query, model_types=None):
        """Return search result from Trello API.

        Parameters
        ----------
        query: str
            String to search against.
        model_types: list | str
            Any combination of the following in a list, or can be a string if only one.
            ['actions', 'boards', 'cards', 'members', 'organizations']
        """
        params = {
            'query': query,
            'modelTypes': model_types,
        }
        response = self._get(['search'], params=params)
        return response

    # TODO ###################################
    def move_list(self, list_id, new_board_id):
        raise NotImplementedError

    def move_card(self, card_id, new_list_id):
        raise NotImplementedError

    # CONVENIENCE #########################
    def get_shared_boards(self):
        """Get boards where there are other members."""
        pass

    def get_private_boards(self):
        """Get boards that have no other members and are set to private."""
        pass

    def get_boards_by_name(self, partial=False):
        pass

    def __repr__(self):
        return('<simpletrello.TrelloCLient>(key={}...{}, token={}...{})'.format(
            self._api_key[0], self._api_key[-1], self._token[0], self._token[-1]))
