import pytest
from flask import session, g
from datetime import date


def test_homepage(client):
    """Test homepage route."""
    response = client.get("/")
    assert response.status_code == 200


"""
User Authentication Tests
"""


def test_user_registration(client, models):
    """Test user registration process."""
    data = {
        "email": "newuser@test.com",
        "username": "newuser",
        "password": "Password123",
        "first_name": "New",
        "last_name": "User",
    }
    response = client.post("/register", data=data, follow_redirects=True)
    assert response.status_code == 200

    user = models["User"].query.filter_by(username="newuser").first()
    assert user is not None
    assert user.email == "newuser@test.com"
    assert user.first_name == "New"

    response = client.post("/register", data=data, follow_redirects=True)
    assert b"This E-mail is already in the database" in response.data

    data2 = {
        "email": "newuser2@test.com",
        "username": "newuser",
        "password": "Password123",
        "first_name": "New 2",
        "last_name": "User",
    }
    response = client.post("/register", data=data2, follow_redirects=True)
    assert b"Error creating new user" in response.data


def test_user_login(client, test_user):
    """Test user login functionality."""
    response = client.post(
        "/login",
        data={"username": "testuser1", "password": "PassWord1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome back Test User" in response.data
    assert b"testuser1" in response.data

    response = client.post(
        "/login",
        data={"username": "testuser1", "password": "WrongPassword"},
        follow_redirects=True,
    )
    assert b"User and/or password invalid" in response.data

    response = client.post(
        "/login",
        data={"username": "nonexistent", "password": "Password123"},
        follow_redirects=True,
    )
    assert b"User and/or password invalid" in response.data


def test_user_logout(client, test_user):
    """Test user logout functionality."""
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"testuser1" not in response.data


"""
User Profile Tests
"""


def test_profile_view(client, test_user):
    """Test profile view and edit functionality."""
    # Login first
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    # Test profile view
    response = client.get("/user")
    assert response.status_code == 200
    assert b"Test User" in response.data

    # Test profile update
    update_data = {
        "email": "updated@test.com",
        "first_name": "Updated",
        "last_name": "User",
        "button": "save",
    }
    response = client.post("/user", data=update_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"User profile updated" in response.data

    # Test password change
    password_data = {
        "password": "PassWord1",
        "new_password": "NewPassWord1",
        "button": "change_password",
    }
    response = client.post("/user", data=password_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Password updated" in response.data


"""
Book Management Tests
"""


def test_add_book_to_user(client, test_user, models):
    """Test adding a book to user's reading list."""
    # Login first
    response = client.post(
        "/login",
        data={"username": "testuser1", "password": "PassWord1"},
        follow_redirects=True,
    )

    # Add book
    book_data = {
        "api_id": "test123",
        "title": "Test Book",
        "authors": ["Test Author"],
        "cover": "https://example.com/cover.jpg",
    }
    response = client.post("/den/add-book", data=book_data, follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert b"Book added to your reading list" in response.data

    # Verify book is in database
    book = models["Book"].query.get("test123")
    assert book is not None
    assert book.title == "Test Book"

    # Test adding same book again
    response = client.post("/den/add-book", data=book_data, follow_redirects=True)
    assert b"Book already in your reading list" in response.data


def test_remove_book_from_user(client, test_user, test_book):
    """Test removing a book from user's reading list."""
    # Login first
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    # Add book to user's list
    test_user.add_to_reading_list(test_book)

    # Remove book
    response = client.post(f"/den/{test_book.api_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Book removed from your reading list" in response.data
    assert test_book not in test_user.books


"""
Book Club Tests
"""


def test_create_club(client, test_user):
    """Test creating a new book club."""
    # Login first
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    # Create club
    club_data = {"name": "Test Club", "description": "A test book club"}
    response = client.post("/clubs", data=club_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Reading club added to the database" in response.data


def test_club_membership(client, test_user, models):
    """Test club membership operations."""
    # Login first
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    # Create a club
    club = models["Club"].create_club(
        name="Test Club", description="Test Description", owner_id=test_user.id
    )

    # Create another user to invite
    new_user = models["User"].signup(
        {
            "email": "test2@test.com",
            "username": "testuser2",
            "password": "PassWord2",
            "first_name": "Test",
            "last_name": "User2",
        }
    )

    # Test inviting user
    response = client.post(
        f"/clubs/{club.id}/add",
        json={"username": "testuser2"},
        content_type="application/json",
    )
    assert response.status_code == 200

    # Test accepting invitation
    client.post("/login", data={"username": "testuser2", "password": "PassWord2"})
    response = client.post(
        f"/clubs/{club.id}/invite", data={"invite": "accept"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"You joined Test Club" in response.data


"""
Message Tests
"""


def test_club_messages(client, test_user, models):
    """Test club message functionality."""
    # Login first
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    # Create a club
    club = models["Club"].create_club(
        name="Test Club", description="Test Description", owner_id=test_user.id
    )

    # Test posting message
    response = client.post(
        f"/clubs/{club.id}/messages",
        json={"message": "Test message"},
        content_type="application/json",
    )
    assert response.status_code == 200

    # Test getting messages
    response = client.get(f"/clubs/{club.id}/messages")
    assert response.status_code == 200
    messages = response.json.get("messages")
    assert len(messages) == 1
    assert messages[0]["message"] == "Test message"

    # Test updating message
    message_id = messages[0]["id"]
    response = client.patch(
        f"/clubs/{club.id}/messages/{message_id}",
        json={"message": "Updated message"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json["message"]["message"] == "Updated message"

    # Test deleting message
    response = client.delete(
        f"/clubs/{club.id}/messages/{message_id}",
        json={},
        content_type="application/json",
    )
    assert response.status_code == 200


def test_protected_routes(client):
    """Test that protected routes require login."""
    routes = [
        "/den",
        "/user",
        "/clubs",
    ]

    for route in routes:
        response = client.get(route, follow_redirects=True)
        assert response.status_code == 200
        assert b"Please login first" in response.data


"""
API Integration Tests
"""


def test_book_search(client, test_user):
    """Test book search API integration."""
    # Login first
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    # Test search with query
    response = client.get("/search?q=python")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)

    # Test empty search
    response = client.get("/search?q=")
    assert response.status_code == 400
    assert "error" in response.json


def test_book_details(client, test_user):
    """Test book details API integration."""
    # Login first
    client.post("/login", data={"username": "testuser1", "password": "PassWord1"})

    # Test getting book details
    response = client.get("/book/gCtazG4ZXlQC")
    assert response.status_code == 200
    data = response.json
    assert "title" in data
    assert "authors" in data
