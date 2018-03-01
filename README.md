# Simpletrello

[![Build Status](https://travis-ci.org/csansone/simpletrello.svg?branch=master)](https://travis-ci.org/csansone/simpletrello)

A simple python wrapper to the Trello API.

**Purpose:** The purpose of this project is to make it as simple as possible to access those features of Trello that are most commonly seen and used in the web GUI, and also likely to have utility in being accessed and modified programmatically.

## Usage

You need your API key and an authorization token.

Get your Trello API key [here](https://trello.com/app-key). There is a link on the page to generate yourself a token.

### Client

Armed with your API key and token, you are ready to instantiate a client.

There are two ways to pass your credentials to the TrelloClient object on creation.

The first is to pass `api_key` and `token` arguments:

```python
from simpletrello import TrelloClient

trello = TrelloClient(
	api_key=<YOUR_API_KEY>,
	token=<YOUR_TOKEN>
)
```

Alternatively, set the following environment variables:

* `SIMPLETRELLO_API_KEY`

* `SIMPLETRELLO_TOKEN`

and call the class with no arguments:

```python
from simpletrello import TrelloClient

trello = TrelloClient()
```

In a bash shell, one way to set these is:

`export SIMPLETRELLO_API_KEY='<your key>' && export SIMPLETRELLO_TOKEN='<your token>'`

The answer [here](https://askubuntu.com/questions/58814/how-do-i-add-environment-variables/58828#58828) goes into more detail, and is archived [here](https://archive.is/Ug6CC) in case the link goes down.

**NOTE:**

The `TrelloClient` object first checks for `api_key` and `token` arguments. If these arguments are passed, environment variables are ignored.

Only if `TrelloClient`is called with no arguments, it will use the environment variables above.

In the event that arguments are not passed and the variables are not set, an `AuthenticationError` will be raised.

*Note: Everything is based on the client described above.*

*Usage docs below will use `trello` to represent a `TrelloCLient` instance as called from the instructions above.*

### Boards

Boards are the highest level structure in a Trello account. The simpletrello library offers several convenience methods to access individual boards or groups of boards.

#### Get a Single Board

Simple and fast, for when you know what board you want.

I have created a demonstration board at https://trello.com/b/xJptH4LM/ and named it *Test Board 001*.

```python
>>> board = trello.get_board('xJptH4LM')
>>> board.name
'Test Board 001'
>>> board.id
'59b20aa457b03ce5735de812'
```

Okay, so we can get a board if we know its URL. Each board (and this is true for most or all other trello structures) also has a unique `id`.

It is probably a good habit to use `id` attributes, but either the `id` or the URL segment after `trello.com/b` will work.

```python
>>> board = trello.get_board('59b20aa457b03ce5735de812')
>>> board.name
'Test Board 001'
>>> board.id
'59b20aa457b03ce5735de812'
```

At the time of this writing (February, 2018), this `id` attribute doesn't seem to be present in any of the web page code, but only is accessible programmatically.

Interestingly, visiting `https://trello.com/b/<BOARD_ID>`, where <BOARD_ID> is the `id` attribute, does redirect to the Trello board with that ID.

#### Create a Board

```python
>>> new_board = trello.create_board('Naming Things is Hard')
>>> new_board.name
'Naming Things is Hard'
>>> new_board.id
'5a94f06be7bd9712d1971d19'
```

#### Get All Boards

This gets all the boards you have access to with your account, including:

- open boards
- closed boards
- boards you admin
- boards where you have been added as a user
- boards you have starred

```python
>>> boards = trello.get_all_boards()
>>> len(boards)
63
>>> for i, board in enumerate(boards):
...     if board.name == 'Test Board 001':
...         print(i)
... 
42
>>> boards[42].name
'Test Board 001'
>>> boards[42].id
'59b20aa457b03ce5735de812'
```

## Tests

Documentation coming soon.

## InsecurePlatformWarning

The `requests` library depends on `urllib3` to do its work.

Certain Python versions (below 2.7.9?) will issue `InsecurePlatformWarning`, along with further instructions that should be read by the user.

https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl-py2
`pip install urllib3[secure]`

pulls in the following additional dependencies:

	asn1crypto==0.22.0
	cffi==1.10.0
	cryptography==2.0.3
	enum34==1.1.6
	ipaddress==1.0.18
	pycparser==2.18
	pyOpenSSL==17.2.0
	six==1.10.0

## License

This software is licensed under the MIT License. Full text in the `LICENSE` file.