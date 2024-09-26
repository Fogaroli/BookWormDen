# Book Wom Den

The Book Worm Den is a web portal for book readers to meet and exchange their knowledge.


## Setup

Make sure you have python installed.
Create a virtual environment and install required packages:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Unit Tests

Unit tests can be executed entering the test folder and triggering the test for each python file that needs to be tested, example below:

`python -m unittest test_<file name>.py`


# Environmental variables

The following items should be set in environmental variables, or saved into a `.env` file inside the src folder.

```
DB_URI=postgresql:///<database name>
TEST_DB_URI=postgresql:///<test database name>
FLASK_DEBUG=1 # Set to zero to disable debug
SECRETE_KEY=<password> # To be used by flask
```