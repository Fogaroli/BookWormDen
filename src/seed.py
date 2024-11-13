"""
File used to enter basic data into the database

"""

import bcrypt
from app import app
from models import db, User, Book, UserBook, Comment
from flask_bcrypt import Bcrypt
from datetime import datetime, date, timedelta

# Clear database
with app.app_context():
    db.drop_all()
    db.create_all()

bcrypt = Bcrypt()

if __name__ == "__main__":
    app.app_context().push()

user1 = User(
    username="fabricio",
    password=bcrypt.generate_password_hash("fabricio").decode("utf8"),
    email="fogaroli@gmail.com",
    first_name="Fabricio",
    last_name="Ribeiro",
    bio="Just trying to get there",
    location="Porto, Portugal",
)

user2 = User(
    username="mainworm",
    password=bcrypt.generate_password_hash("bigworm").decode("utf8"),
    email="bfworm@test.com",
    first_name="Main",
    last_name="Worm",
)

user3 = User(
    username="bookworm42",
    password=bcrypt.generate_password_hash("password123").decode("utf8"),
    email="bookworm42@example.com",
    first_name="Sarah",
    last_name="Johnson",
    bio="Avid reader and fantasy lover",
    location="Seattle, WA",
)

db.session.add_all([user1, user2, user3])
db.session.commit()

books_data = [
    {
        "api_id": "gCtazG4ZXlQC",
        "title": "Harry Potter and the Deathly Hallows",
        "cover": "http://books.google.com/books/content?id=gCtazG4ZXlQC&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE71LN9CVUejqkZ5y9DkDZ6b_zNd6FZBlKjYNshG1NTvt0tHKZDV15bg3YlQkpvnLC4Fhxhmp4rVEVUsl_LX4YwlM1aTgovYBotqZrz-4S5cJBxRNbVHPnPLW3HuNs-75avK9BnCq&source=gbs_api",
        "authors": "J.K. Rowling",
        "categories": "Juvenile Fiction / Action & Adventure / General,Fiction / Action & Adventure,Fiction / Fantasy / Contemporary,Juvenile Fiction / Fantasy & Magic,Young Adult Fiction / Action & Adventure / General,Young Adult Fiction / Fantasy / Wizards & Witches,Young Adult Fiction / School & Education / Boarding School & Prep School,Juvenile Fiction / School & Education,Fiction / Fantasy / General",
        "description": "<p><i>'Give me Harry Potter,' said Voldemort's voice, 'and none shall be harmed. Give me Harry Potter, and I shall leave the school untouched. Give me Harry Potter, and you will be rewarded.'</i><br><br>As he climbs into the sidecar of Hagrid's motorbike and takes to the skies, leaving Privet Drive for the last time, Harry Potter knows that Lord Voldemort and the Death Eaters are not far behind. The protective charm that has kept Harry safe until now is broken, but he cannot keep hiding. The Dark Lord is breathing fear into everything Harry loves and to stop him Harry will have to find and destroy the remaining Horcruxes. The final battle must begin - Harry must stand and face his enemy...<br><br><br><i>Having become classics of our time, the Harry Potter eBooks never fail to bring comfort and escapism. With their message of hope, belonging and the enduring power of truth and love, the story of the Boy Who Lived continues to delight generations of new readers.</i></p>",
        "page_count": 784,
    },
    {
        "api_id": "mWVXEAAAQBAJ",
        "title": "The Culture and Communities Mapping Project",
        "cover": "http://books.google.com/books/publisher/content?id=mWVXEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE72Zc5CtHd8aTAvBAjb9MZAgyzttMqW9AHGbwXu78HYt9TYTBwk9rAFwJtSJKLrlE8YuNjwZQf4dTWDIMGpKJZ5KcNGtHaJhfDWI4JjmrveFUX08QNH-EuSjd8GacvNoGXHv0jtI&source=gbs_api",
        "authors": "Morgan Currie,Melisa Miranda Correa",
        "categories": "Social Science / Sociology / General,Social Science / Human Geography,Language Arts & Disciplines / Library & Information Science / General,Computers / Data Science / General,Science / Earth Sciences / Geography,Literary Criticism / General,Computers / General,Social Science / Anthropology / Cultural & Social",
        "description": "<p>This book describes three years of work by the Culture and Communities Mapping Project, a research project based in Edinburgh that uses maps as an object of study and also a means to facilitate research. Taking a self-reflexive approach, the book draws on a variety of iterative mapping procedures and visual methodologies, from online virtual tours to photo elicitation, to capture the voices of inhabitants and their distinctive perspectives on the city. The book argues that practices of cultural mapping consist of a research field in and of itself, and it situates this work in relation to other areas of research and practice, including critical cartography, cultural geography, critical GIS, activist mapping and artist maps. The book also offers a range of practical approaches towards using print and web-based maps to give visibility to spaces traditionally left out of city representations but that are important to the local communities that use them. Throughout, the authors reflect critically on how, through the processes of mapping, we create knowledge about space, place, community and culture.</p><p></p>",
        "page_count": 122,
    },
    {
        "api_id": "zU8ZAwAAQBAJ",
        "title": "Bridging UX and Web Development",
        "cover": "http://books.google.com/books/publisher/content?id=zU8ZAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70jHN4_6pfRy40onWL1_AjwUzyMiTAR9e6p9bUhsSFMyXthtTMp8T83Qm_V60tC2CY4qWM-JvUrvjxfvneUh2K7suIgWM7-dH5lwy-P-O04E0hFWfjrma7jM9eakQ_6m8W6djKG&source=gbs_api",
        "authors": "Jack Moffett",
        "categories": "Computers / Internet / General,Computers / Human-Computer Interaction (HCI)",
        "description": "The divide between UX and Web development can be stifling. Bridging UX and Web Development prepares you to break down those walls by teaching you how to integrate with your team's developers. You examine the process from their perspective, discovering tools and coding principles that will help you bridge the gap between design and implementation. With these tried and true approaches, you'll be able to capitalize on a more productive work environment. Whether you're a novice UX professional finding your place in the software industry and looking to nail down your technical skills, or a seasoned UI designer looking for practical information on how to integrate your team with development, this is the must-have resource for your UX library. - Establish a collaboration lifecycle, mapping design activities to counterparts in the software development process - Learn about software tools that will improve productivity and collaboration - Work through step-by-step exercises that teach font-end coding principles to improve your prototyping and implementation activities - Discover practical, usable HTML and CSS examples - Uncover tips for working with various developer personas.",
        "page_count": 224,
    },
]

today = date.today()

# Create books
created_books = []
for book in books_data:
    new_book = Book.saveBook(book)

comments_data = [
    {
        "user_id": 1,
        "book_id": "gCtazG4ZXlQC",
        "comment": "A perfect ending to an amazing series. The way everything comes together is brilliant!",
        "rating": 5.0,
        "domain": 2,  # Public
        "date": today - timedelta(days=15),
    },
    {
        "user_id": 2,
        "book_id": "mWVXEAAAQBAJ",
        "comment": "Fascinating research on cultural mapping. Very relevant for urban studies.",
        "rating": 4.5,
        "domain": 2,  # Public
        "date": today - timedelta(days=12),
    },
    {
        "user_id": 3,
        "book_id": "zU8ZAwAAQBAJ",
        "comment": "Essential reading for anyone working in web development teams.",
        "rating": 4.8,
        "domain": 1,  # Internal
        "date": today - timedelta(days=10),
    },
    {
        "user_id": 1,
        "book_id": "zU8ZAwAAQBAJ",
        "comment": "Great practical advice for bridging the design-development gap.",
        "rating": 4.7,
        "domain": 2,  # Public
        "date": today - timedelta(days=8),
    },
    {
        "user_id": 1,
        "book_id": "mWVXEAAAQBAJ",
        "comment": "Re-reading this book never gets old. Always find new details!",
        "rating": 4.9,
        "domain": 1,  # private
        "date": today - timedelta(days=5),
    },
    {
        "user_id": 2,
        "book_id": "gCtazG4ZXlQC",
        "comment": "Interesting at most",
        "rating": 2.0,
        "domain": 2,  # Public
        "date": today - timedelta(days=2),
    },
]

# Create comments
for comment_data in comments_data:
    new_comment = Comment(**comment_data)
    db.session.add(new_comment)
    db.session.commit()


userbooks_data = [
    {
        "user_id": 1,
        "book_id": "gCtazG4ZXlQC",
        "start_date": today - timedelta(days=30),
        "finish_date": today - timedelta(days=5),
        "current_page": 784,  # Completed
        "status": 3,  # Completed
    },
    {
        "user_id": 1,
        "book_id": "mWVXEAAAQBAJ",
        "start_date": today - timedelta(days=10),
        "finish_date": None,
        "current_page": 45,
        "status": 1,  # Currently reading
    },
    {
        "user_id": 1,
        "book_id": "zU8ZAwAAQBAJ",
        "start_date": None,
        "finish_date": None,
        "current_page": 0,
        "status": 0,  # Backlog
    },
    {
        "user_id": 2,
        "book_id": "gCtazG4ZXlQC",
        "start_date": today - timedelta(days=60),
        "finish_date": today - timedelta(days=40),
        "current_page": 784,
        "status": 3,  # Completed
    },
    {
        "user_id": 2,
        "book_id": "zU8ZAwAAQBAJ",
        "start_date": today - timedelta(days=15),
        "finish_date": None,
        "current_page": 98,
        "status": 2,  # Postponed
    },
    {
        "user_id": 3,
        "book_id": "zU8ZAwAAQBAJ",
        "start_date": today - timedelta(days=20),
        "finish_date": today - timedelta(days=2),
        "current_page": 224,
        "status": 3,  # Completed
    },
    {
        "user_id": 3,
        "book_id": "gCtazG4ZXlQC",
        "start_date": today - timedelta(days=5),
        "finish_date": None,
        "current_page": 350,
        "status": 1,  # Currently reading
    },
    {
        "user_id": 3,
        "book_id": "mWVXEAAAQBAJ",
        "start_date": None,
        "finish_date": None,
        "current_page": 0,
        "status": 0,  # Backlog
    },
]

for readlog in userbooks_data:
    new_readlog = UserBook(**readlog)
    db.session.add(new_readlog)
    db.session.commit()
