# The Bookwom Den

A web portal for book readers to meet and exchange their knowledge.

The Bookworm Den is an education project intended to be delivered as a capstone project for the first half of the Software Engineering Course from Springboard.

The main features of this portal is to allow people passionate about books, to create a personal reading list where they cna register books that they are read, the ones they are currently reading adn a list of upcoming books to read. In addition the portal allow users to create reading clubs, where users can connect to share books they want to read together and raise discussions about the topics they want.

## Features

1. Using the Bookworm Den portal visitors can search for books based on the book title and read a public description about the book, among the information the user can find authors, publishers and other additional information. The book information is provided by using the Google Books API and results are filtered to english books only.  
    - If the user has created an account withing the portal, after finding the book on the search mechanism they can add the book to their reading list.

1. Once the user is logged they have access to their own Den, which is a space dedicated to show all the books they have added to their list and the status of the reading, which includes start and finish date, the page they are at and if they have completed reading the book.

1. Once entering in one of the books form their reading list, they can review the book description, update the data related to the reading status, book comments created by other users of the Bookworm Den. In addition users can add their own comment about the book and add it to a reading club that they are member.

1. Book comments can be marked as public or private, private comments are only viewed by the person that created it, public comments are available to other registered members of the Den.

1. The major feature of the Den comes with the creation of reading clubs. Any user can create a reading club and invite other members to join. Any member when receiving a joining invite can either accept to become a member of the club or reject the membership.  NOTE. Only the creator of the reading club can add or remove members from the club.

    1. Once a member of a reading club, any user can contribute with books to the club reading list and post messages on the forum, found on the reading club page.
    1. Similar to the membership any book added to the club reading list can only be deleted by the club creator.
    1. The discussion forum created within a reading club allow users to share ideas and raise discussions, the members area allowed to edit or delete their own messages, but cannot delete message from other users.

## The project

This project is developed using a backend written in Python Flask and front end using vanilla javascript, the details of the technologies are documented in the [BookwormDen_Description](./documentation/BookwormDen_Description.md).

The development steps and tasks are documented in the [Project_Steps](./documentation/Project_Steps.md) document.

## Deployment

The BookwormDen web application is planned to be deployed to 2 different instances:

A development server, running the latest code found on the `dev` branch. It can be accessed on the link https://dev-bookwormden.onrender.com.

A production server, running the latest code found on the `main` branch. It can be accessed on the link https://bookwormden.onrender.com



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
SECRETE_KEY=<a passphrase of your choice> # To be used by flask
GOOGLE_API_KEY=<key generated on google API with access to goog books> # Used to search for new books from Google Books
```

## Run

The source code for the application is found on /src. It is possible to run the web application locally by starting flask internal web app using:

`flask run`

Run in debug mode by using

`flask run --debug`

## Unit Tests

Unit tests are written and added to the repository. 
Backend tests can be executed entering the `src/backend_unit_test` folder and triggering each python test script individually, example below:

`python -m pytest test_<file name>.py`

Frontend tests are developped in Node.js Jest, it is necessary to have node installed on the machine that will be used to run the tests.
Navigate to the `src`folder and use:

`npm install`
`npm run test`
