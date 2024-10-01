# Book Wom Den

The Book Worm Den is a web portal for book readers to meet and exchange their knowledge.

The application is developed using a backend written in Python Flask, the details of hte technologies should be documented in the `docs` folder.

The development steps and tasks are documented in the `Project Structure`document inside the `src` folder.



## Deployment

The BookWormDen web application is planned to be deployed to 2 different instances:

A development server, running the latest code found on the dev branch. It can be accessed on the link https://dev-bookwormden.onrender.com.

A production server, running the latest code found on the main branch. URL TBD



# Run the app locally

## Setup

Make sure you have python installed.
Create a virtual environment and install required packages:

```
python3 -m venv .venv
source .venv/bin/activate
```
Inside the src folder execute:
```
pip install -r requirements.txt
```

Create a local PostgreSQL database and create a .env file inside the src folder with the database name.
The .env file should contain the variables:

```
DB_URI=postgresql:///<database name>
TEST_DB_URI=postgresql:///<test database name>
SECRETE_KEY=<password> # To be used by flask
```

## run

The source code for the application is found on /src. It is possible to run the web application locally by starting flask internal web app using:

`flask run`

Run in debug mode by using

`flask run --debug`

## Unit Tests

Unit tests are written and added to the repository. They can be executed entering the `test` folder and triggering each python test script individually, example below:

`python -m unittest test_<file name>.py`


