# The BookWormDen project document

This document describes the project structure and steps to be followed in order to complete the project design.

## Considerations

- Detailed documentation about the project should be created along with the project.
- Unit testing should be developed along with the features implemented, and not accumulated to the end of the project.
- Continuous deployment should be considered if the site hosting platform allows, to streamline the steps from features implementation to production.
- The repository should be organized in 3 basic branch category. The Main branch should store the production quality product. Only after the complete MVP is completed data should be pulled to Main. The dev branch should accumulate all new features implemented, in order to be validated before being pulled into production. Feature and bugfix branch should be derived from the dev branch and once completed and tested should be merged into dev.

## Assumptions

- 

## Project developemnt steps:

1. Create base Flask structure and HTML templates using local database.
2. Created database models for user accounts.
3. Create registration/login functionality, with active sessions saved on Flask Sessions.
4. Create Book search API engine.
5. Create Book Search interface and result management. Should differentiate between unsigned and signed users.
6. Create database model for books information.
7. Create interface to store books in the database.
8. Create functionality for users to log reading status and statistics (associated database model update/creation).
9. Create model for book clubs.
10. Create functionality to create book clubs (Create clubs, add users, add book reading list)
11. Create book feedback/comments functionality (differentiate private and public comments, update search engine logic to include locally stored feedback).
12. Create message board within the club.
<To be Expanded>