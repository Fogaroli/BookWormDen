# Capstone Project I

This is the first capstone project for the Springboard Software Engineering Track. This project should include all technologies taught in the course up to this point.
The final product should be a database-driven website powered by an API (either external or included int he project).

The main technologies to be included:

1. Flask for Backend development + Jinja
2. WTForms
3. SQLAlchemy
4. PosgreSQL
5. Javascript for frontend development
6. Ajax for API interface
7. CSS and Boostrap for styling
8. JQuery

## Step Two - Project Proposal

This document describes in further details the project proposal for the Capstone Project I.

## Book Club Platform

The project intends to crete a book club platform, which will be used by the community to create reading groups, which will allow sharing book feedback, book reading list and foment discussions among peers that share the love to read.

The platform will have a public and private area, where any participant can feel safe about publishing their perspective about any book they have read to a group of people they know and also view comments from group peers to help decide which book to read next.

The platform should connect to remote servers to allow searching for new books and add them to their reading list.

### Functionality details

Access to the platform is controlled by user login, non-logged users will have access to a search engine to look for books based on their title or author and will have access to __Public__ comments posted by the users.

>Challenge 1: Design a login process that would allow the user to create a local account for the platform or login using their google account credentials.

Once the user is logged additionally to the search service above they can:

- View statistics about their reading and accomplishments (number of book read, average time per book)
- View and edit which book they are reading now, with the comments published about that book, either public or published by members of reading groups which they currently belong.
- Access any reading group that they already belong.
- Create a reading group.

>Stretch 1: Create a group searching engine and allow user to request to join an existing group.

When entering a reserved reading group space (only the owner and group member will have access to this page) the user can access:

- Message board, which are messages left on the group page (a blog style page with messages posted by any user)
- View club reading list (which are books added by any member of the club intended to be discussed within the group)
- Access private book comments published by members of the groups (These are comments not displayed in the public book search engine)
- Review reading statistics from other members of the club.
- If owner of the group, search and any new members to the group.
- If owner of the group remove books from the reading list.
- If owner remove other users from the group.

At any screen logged in users, when searching for new books will have access to the information of the books, public and private comments from that book (private only from members that share a reading club with the logged user), add the book as currently being read, and/or add the book to the reading list of any club they belong.

> Challenge 2: When searching for the book, the system would pull up the current price of the book on a online store (e.g. amazon).

When the user starts reading a book, they can record that information in the private area of the platform, with the date they started reading. Once they have finished it they can record the date and the system will add the data to the user reading statistics.
Additionally, after reading the book, the user can publish private or public comments of the book to be available for other users.

> Stretch 2: The user should be able to record partially read books and which page they stopped before switching to a new book, and once they return to the unfinished book they have the information to start from where they left off. The system would allow to date ranges to properly calculate the time spent reading the book.


### Internal Structure

The platform will be developed in Flask using Jinja2 to render HTML templates to the frontend. Some functionalities will be managed totally in the frontend using javascript supplied by Flask to the user's browser.

The data will be stored in a PostgreSQL database hosted on a third party free database hosting service (e.g. Supabase, ElephantSQL)

Frontend styling should be done using Bootstrap.

The split functionality between backend and frontend will be adjust during development in order to improve reliability of the platform, but the initial proposal is:

##### Backend
- Homepage rendering.
- Book serch
- Connection to library API for book search
- Handle User login and open session
- Handle access control to reading groups
- Reading statistics
- Reading group information
- Internal RestfulAPI for book comments.
- Internal RestfulAPI for reading group discussion interface. 

##### Frontend
- Dinamically expose/hide book search interface
- AJAX connection to backend to read book comments when a book is selected.
- AJAX connection to backend to render reading group discussion page.
- Interface customizations (stored in cookies)

### Database

The data used by the platform will use PostgreSQL and should be hosted by a third party database service.

The proposed structure is described in the tables below:

| table: users | Summary|
|---|---|
| id|Primary Key|
|username| unique|
|password| encrypted data|
|First Name||
|Last Name||
|\<profile information>| Profile data to be defined|

| table: books | Summary|
|---|---|
| id|Primary Key|
|title| unique|
|author||
|ISBN||

|table: comments| Summary|
|---|---|
|user_id| Foreign Key, Primary Key|
|book_id| Foreign Key, Primary Key|
|comment| |
|public| Binary Flag|

|table: user_book| Summary|
|---|---|
|user_id| Foreign Key, Primary Key|
|book_id| Foreign Key, Primary Key|
|start_date|datetime|
|finish_date|datetime|
|page stopped||
|status|0-wishlist, 1-reading, 2-completed|

| table: group | Summary|
|---|---|
| id|Primary Key|
|owner_id| Foreign Key (Users)|
|Group Name||
|Group Description||
|\<profile information>| Profile data to be defined|

|table: members | Summary|
|---|---|
|group_id| Foreign Key|
|user_id| Foreign Key|

|table: readlist | Summary|
|---|---|
|group_id| Foreign Key|
|book_id| Foreign Key|

|table: blog | Summary|
|---|---|
|group_id| Foreign Key|
|author_id| Foreign Key (user)|
|message||
|timestamp|datatime|

### Questions

1. Focus:
    The platform will have functionalities implemented in the solely in the backend, functionalities implemented in the frontend and few features will use resources from both, the exact proportion is still unclear, but the intent is for a full-stack application.

2. Tech Stack:
    The platform will use Flask/Jinja, matched with "vanilla" javascript in the frontend with Bootstrap css framework, AJAX (maybe JQuery). DAtabase based in PostgreSQL

3. Type:
    Website, with full compatibility to run on small screen devices (mobile phone browser)

4. Goal:
    Design a platform to help friends and family to share they passion for books by creating safe environments to write book comments and coordinate group readings.

5. Users:
    Friends and family members interested in creating a reading group to coordinate book readings and share information. This can even be used in schools to create reading activities and prepare for book challenges ("Battle of the books").

6. Data:
    Book information will be extracted from online library APIs, providing name, author, short description and book code. This data can be used to generate requests to other sources of information to collect additional information (e.g. book price).
    Bok comments and reading group conversations are private to the website and the information will be be shared for any other purpose.

### Risks

1. The platform will use a complex database structure, this will increase complexity of the product.
2. External information sources (API) might be unstable or not available for the posted website.