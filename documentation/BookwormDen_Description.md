# The  Bookworm Den

The project completed the first cycle fo the course consolidating the knowledge acquired to that point.

In the attempt to use most if not all the functionality learned, the project encapsulates multiple technologies using a mix of code format, in order to explore and practice the use of different tools, libraries and concepts.

The full stack project is divided into a backend written in Python making use of the Flask framework and using Jinja to render html templates. The frontend is written in Vanilla javascript, using a mix of basic javascript and JQuery, along with Bootstrap css library for styling.

## Backend

For the backend implementation the project focus on the usage of Flask to manage the http request and responses. Additional libraries used are:

1. WTForms to manage form data.
1. SQLAlchemy to manage the database
1. BCrypt to manage password encryption
1. Jinja to render html templates
1. PyTest for unit testing

The backend files are split into a main [app.py](../src/app.py) that consolidates all http routes.
The database model and management is all concentrated into the [models.py](../src/models.py).
All form data, with its additional validator functions are created in the [forms.py](../src/forms.py).

To manage the data used in the project a relational database was created using PostgreSQL, the database modelling can be visualized in the file [Database](./Database.md)

## Frontend

For the frontend implementation the project uses Vanilla Javascript with assistance of the libraries below:

1. JQuery for DOM manipulation
1. Bootstrap for CSS styling
1. Axios for API requests to the backend.
1. Jest for unit testing.
1. FontAwesome for icon images.

The Javascript code is split among multiple files, being rendered according to the html template loaded by the backend. It is possible to notice that some files make use of JQuery and others don't, this is a intentional difference to make sure that DOM manipulation is practiced with and without the use of JQuery.

The javascript file [classes.js](../src/static/classes.js) concentrates all classes written in javascript and it is accessed by multiple script files.
The file [app.js](../src/static/app.js) concentrates the handling of the book search engine, present in the navigation bar.
The remaining javascript files are loaded by specific HTML templates to handle data on those pages.

The intention to not load all script files in the base html template is to avoid overloading the client with javascript code that is not being used.
