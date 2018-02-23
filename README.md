#simpletrello

[![Build Status](https://travis-ci.org/csansone/simpletrello.svg?branch=master)](https://travis-ci.org/csansone/simpletrello)

A simple python wrapper to the Trello API.

**Purpose:** The purpose of this project is to make it as simple as possible to access those features of Trello that are most commonly seen and used in the web GUI, and also likely to have utility in being accessed and modified programmatically.

##Quickstart

You need your API key and an authorization token.

Get you Trello API key [here](https://trello.com/app-key). There is a link on the page to generate yourself a token.

###Client

Armed with your API key and token, you are ready to instantiate a client.

There are two ways to pass your credentials to the TrelloClient object on creation.

The first is to pass `api_key` and `token` arguments:

```
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

```
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

---

##Tests

---

##InsecurePlatformWarning

The `requests` library depends on `urllib3` to do its work.

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


---

##License

This software is licensed under the MIT License. Full text in the `LICENSE` file.