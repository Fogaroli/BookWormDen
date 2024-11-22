``` Mermaid
classDiagram
    User "1" -- "*" UserBook : has
    User "1" -- "*" Comment : makes
    User "1" -- "*" ClubMembers : has
    User "1" -- "*" Message : posts
    Book "1" -- "*" UserBook : has
    Book "1" -- "*" Comment : has
    Book "1" -- "*" ClubBook : has
    Club "1" -- "*" ClubMembers : has
    Club "1" -- "*" ClubBook : has
    Club "1" -- "*" Message : contains

    class User {
        Field | Type
        ---|---
        id | Integer
        username | String(30)
        password | Text
        first_name | String(50)
        last_name | String(50)
        email | String(100)
        image_url | Text
        bio | Text
        location | String(30)
        Methods | Return
        validate_user(password) | User/False
        update_info(data) | User/False
        update_password(new_password) | User/False
        $signup(data) | User/False
    }

    class Book {
        Field | Type
        ---|---
        api_id | String(30)
        title | Text
        cover | Text
        authors | Text
        categories | Text
        description | Text
        page_count | Integer
        Methods | Return
        $saveBook(data) | Book/False
    }

    class UserBook {
        Field | Type
        ---|---
        user_id | Integer FK
        book_id | String FK
        start_date | Date
        finish_date | Date
        current_page | Integer
        status | Integer
        Methods | Return
        delete() | Boolean
    }

    class Comment {
        Field | Type
        ---|---
        user_id | Integer FK
        book_id | String FK
        date | Date
        comment | Text
        rating | Numeric
        domain | Integer
        Methods | Return
        serialize() | Dict
    }

    class Club {
        Field | Type
        ---|---
        id | Integer
        name | String
        description | Text
        Methods | Return
        update(name, description) | Boolean
        delete() | Boolean
        add_book_to_list(book) | Boolean
        $create_club(name, description, owner_id) | Club/False
    }

    class ClubBook {
        Field | Type
        ---|---
        club_id | Integer FK
        book_id | String FK
        Methods | Return
        delete() | Boolean
    }

    class ClubMembers {
        Field | Type
        ---|---
        club_id | Integer FK
        member_id | Integer FK
        status | Integer
        Methods | Return
        accept_invite() | Boolean
        reject_invite() | Boolean
        delete() | Boolean
        $enrol_user(club_id, member_id, status) | ClubMembers/False
    }

    class Message {
        Field | Type
        ---|---
        id | Integer
        club_id | Integer FK
        user_id | Integer FK
        message | Text
        timestamp | DateTime
        Methods | Return
        serialize() | Dict
        delete() | Boolean
        update_message(message) | Message/False
        $add_message(club_id, user_id, message) | Message/False
    }
```