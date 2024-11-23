# The BookwormDen project document

This document describes the project structure and steps to be followed in order to complete the project design.

## Considerations

- Detailed documentation about the project should be created along with the project.
- ~~Unit testing should be developed along with the features implemented, and not accumulated to the end of the project. ~~ Due to challenges to create unit testing and project time constraints, the development focussed into delivering the project MVP and documentation ready as soon as possible, and creating the unit testing in the end, intended to control any regressions during future improvements.
- Continuous deployment should be considered if the site hosting platform allows, to streamline the steps from features implementation to production.
- The repository should be organized in 3 basic branch category. The Main branch should store the production quality product. Only after the complete MVP is completed data should be pulled to Main. The dev branch should accumulate all new features implemented, in order to be validated before being pulled into production. Feature and bugfix branch should be derived from the dev branch and once completed and tested should be merged into dev.

## Assumptions

## Project development steps

1. ~~Create base Flask structure and HTML templates using local database.~~
1. ~~Created database models for user accounts.~~
1. ~~Create registration/login functionality, with active sessions saved on Flask Sessions.~~
1. ~~Integrate supabase database and deploy dev branch to render~~
1. ~~Create Book search API engine (Implemented on the frontend?)~~
1. ~~Create Book Search interface and result management.~~
1. ~~Create a book view page with book content. Should differentiate between signed-in users and anonymous.~~
1. ~~Create database model for books information.~~
1. ~~Create interface to store books in the database.~~
1. ~~Create functionality for users to log reading status and statistics (associated database model update/creation).~~
1. ~~Create model for book clubs.~~
1. ~~Create functionality to create book clubs (Create clubs, add users)~~
1. ~~Add functionality to add books to the club reading list.~~
1. ~~Create book feedback/comments functionality (differentiate private and public comments, update search engine logic to include locally stored feedback).~~
1. ~~Users feedback could be set to private (only to themselves), Friends (Only for people that share a book club), Public (all Den's users). Anonymous users cannot see any review.~~ (Friends is not an option anymore, either public or private)
1. ~~Create RESTful api to handle a message board within the club.~~
1. ~~Create message board frontend~~
1. ~~Book view could have multiple tabs, one for public comments / reviews if available in the API, one for "Den" reviews, other the user to record information about the reading status, and one for the users review. (the data for each tab is build within other tasks below)~~

Features to be added.

- Improve appearance in the entire site
- Add password reset option using the registered E-mail for a temporary password.
- ~~Migrate Unittest to use Pytest~~
- Add Google user Signin option (Might not be a good idea anymore)
- Add dropdown for books already in the database during book search
- Add option for advanced search, MVP only book title search.
- Add an option to mark a feedback abusive, ir multiple reports are received, feedback is marked as private and notification sent to the owner.
- Improve rating on book search to use half start grading
- Order names on the club members list.
