import pytest
from datetime import date, datetime


def test_user_model_creation(models, context):
    """Test basic user model creation"""

    user = models["User"].signup(
        {
            "email": "test@test.com",
            "username": "testuser",
            "password": "PassWord1",
            "first_name": "Test",
            "last_name": "User",
        }
    )

    assert user.username == "testuser"
    assert user.email == "test@test.com"
    assert user.first_name == "Test"
    assert user.password != "PassWord1"


def test_user_authentication(test_user):
    """Test user password validation"""
    assert test_user.validate_user("PassWord1") == test_user
    assert test_user.validate_user("WrongPassword") == False


def test_user_update(test_user):
    """Test user information update"""
    updated = test_user.update_info(
        {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@test.com",
            "image_url": "new_image.jpg",
            "bio": "New bio",
            "location": "New location",
        }
    )

    assert updated.first_name == "Updated"
    assert updated.last_name == "Name"
    assert updated.email == "updated@test.com"
    assert updated.image_url == "new_image.jpg"
    assert updated.bio == "New bio"
    assert updated.location == "New location"


def test_user_password_update(test_user):
    """Test password update functionality"""
    updated = test_user.update_password("NewPassWord2")
    assert updated.validate_user("NewPassWord2") == updated
    assert updated.validate_user("PassWord1") == False


def test_book_model_creation(models, context):
    """Test basic book model creation"""
    book = models["Book"].save_book(
        {
            "api_id": "test123",
            "title": "Test Book",
            "cover": "cover.jpg",
            "authors": "Test Author",
            "categories": "Fiction",
            "description": "Test description",
            "page_count": 200,
        }
    )

    assert book.api_id == "test123"
    assert book.title == "Test Book"
    assert book.cover == "cover.jpg"
    assert book.authors == "Test Author"
    assert book.page_count == 200


def test_user_book_relationship(test_user, test_book):
    """Test adding book to user's reading list"""
    books = test_user.add_to_reading_list(test_book)
    assert test_book in test_user.books
    assert len(books) == 1


def test_user_book_log(models, test_user, test_book):
    """Test UserBook logging functionality"""

    test_user.add_to_reading_list(test_book)
    user_book = (
        models["UserBook"]
        .query.filter_by(user_id=test_user.id, book_id=test_book.api_id)
        .first()
    )

    updated = user_book.update_info(
        {"start_date": date.today(), "current_page": 50, "status": 1}
    )

    assert updated.current_page == 50
    assert updated.status == 1
    assert updated.start_date == date.today()


def test_comment_functionality(models, test_user, test_book):
    """Test comment creation and management"""

    comment = models["Comment"].create_comment(
        {
            "user_id": test_user.id,
            "book_id": test_book.api_id,
            "date": date.today(),
            "comment": "Great book!",
            "rating": 4.5,
            "domain": 1,
        }
    )

    assert comment.comment == "Great book!"
    assert comment.rating == 4.5
    assert comment.user_id == test_user.id

    updated = comment.update({"comment": "Updated comment", "rating": 5.0, "domain": 2})
    assert updated.comment == "Updated comment"
    assert updated.rating == 5.0
    assert updated.domain == 2


def test_club_functionality(models, test_user):
    """Test reading club creation and management"""
    Club = models["Club"]

    # Create club
    club = Club.create_club(
        name="Test Club", description="Test Description", owner_id=test_user.id
    )

    assert club.name == "Test Club"
    assert club.description == "Test Description"

    # Test club update
    updated = club.update("Updated Club", "Updated Description")
    assert updated == True
    assert club.name == "Updated Club"
    assert club.description == "Updated Description"


def test_club_membership(models, test_user):
    """Test club membership management"""
    user2 = models["User"].signup(
        {
            "email": "test2@test.com",
            "username": "testuser2",
            "password": "PassWord2",
            "first_name": "Test2",
            "last_name": "User2",
        }
    )

    club = models["Club"].create_club(
        name="Test Club", description="Test Description", owner_id=test_user.id
    )

    membership = models["ClubMembers"].enrol_user(
        club_id=club.id,
        member_id=user2.id,
        status=3,
    )

    assert membership.status == 3

    assert membership.accept_invite() == True
    assert membership.status == 2


def test_message_functionality(models, test_user):
    """Test club message functionality"""
    club = models["Club"].create_club(
        name="Test Club", description="Test Description", owner_id=test_user.id
    )

    message = models["Message"].add_message(
        club_id=club.id, user_id=test_user.id, message="Test message"
    )

    assert message.message == "Test message"
    assert message.user_id == test_user.id
    assert message.club_id == club.id

    updated = message.update_message("Updated message")
    assert updated.message == "Updated message"

    serialized = message.serialize()
    assert serialized["message"] == "Updated message"
    assert serialized["user_first_name"] == test_user.first_name


def test_delete_operations(models, test_user, test_book):
    """Test various delete operations"""
    Club = models["Club"]
    Message = models["Message"]

    club = Club.create_club(
        name="Test Club", description="Test Description", owner_id=test_user.id
    )

    message = Message.add_message(
        club_id=club.id, user_id=test_user.id, message="Test message"
    )

    assert message.delete() == True
    assert Message.query.get(message.id) is None

    assert club.delete() == True
    assert Club.query.get(club.id) is None

    test_user.add_to_reading_list(test_book)
    user_book = (
        models["UserBook"]
        .query.filter_by(user_id=test_user.id, book_id=test_book.api_id)
        .first()
    )
    assert user_book.delete() == True
