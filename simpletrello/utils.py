# coding: utf-8
"""utils.py"""

from __future__ import print_function, unicode_literals
from random import randint


def listify(data):
    """Check if input is a list. If not, make it a single item list.
    Used for functions designed to operate on multiple objects,
    when only performing operations on a single object.

    Params
    ------
    data: list or single object

    Returns
    -------
    data: list
        Same list as passed in, or single item list.
    """
    if type(data) == list:
        return data
    return [data]


def combine_values(param_items):
    """Return a <value> suitable for a <name=value> URL parameter.

    Params
    ------
    param_items: str or list of str
        Strings to be joined by comma.

    Returns
    -------
    param_string: str

    Examples
    --------
    >>> create_url_parameter('boards')
    >>> 'boards'

    >>> create_url_parameter_value(['boards', 'cards', 'members'])
    >>> 'boards,cards,members'
    """

    param_items = listify(param_items)
    param_string = ','.join(param_items)
    return param_string


def is_stringy(something):
    """Determine if something is a string or Unicode object
    in a manner that is compatible with py2 and py3.

    Returns
    -------
    True|False

    Notes
    -----

    """
    try:
        return isinstance(something, (str, unicode))
    except NameError:
        return isinstance(something, str)


def create_random_text(num_chars):
    chars = (str(randint(0, 9)) for _ in range(num_chars))
    random_text = ''.join(chars)
    return random_text
