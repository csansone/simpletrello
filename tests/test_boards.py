# coding: utf-8
"""test_boards.py"""

import pytest
from requests.exceptions import HTTPError


class TestBoardStuff(object):

    def test_get_board(self, client, board_id_existing):
        board = client.get_board(board_id_existing)
        assert board.id == board_id_existing
        assert isinstance(board.lists, list)
        assert len(board.lists) > 0
        assert 'simpletrello.listobject.List' in repr(board.lists[0])


def test_search_boards_by_name(client):
    boards = client.search_boards_by_name('Never ever should there be a board named like this')
    assert isinstance(boards, list)
    assert len(boards) == 0


def test_create_board_just_name(client, testid):
    board_name = '_test {}'.format(testid)
    board = client.create_board(board_name)
    assert board.name == board_name
    assert board.closed is False
    board_id = board.id
    board.archive()
    # Fresh retreival of board to ensure the server shows it as closed,
    # ruling out local side effects
    board_again = client.get_board(board_id)
    assert board_again.closed is True
    board.delete()
    # Expect an error trying to call board that has been properly deleted
    with pytest.raises(HTTPError):
        client.get_board(board_id)


def test_get_board(client):
    b = client.get_board('XOKUY03O')
    assert b.name.lower() == 'things to test'
