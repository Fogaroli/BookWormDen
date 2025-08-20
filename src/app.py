"""
================================================================
Title: BookWorm Den
Author: Fabricio Ribeiro
Date: September 17, 2024

================================================================
"""
import os
from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    session,
    g,
    url_for,
    request,
    jsonify,
)
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from models import (
    # ClubBook,
    db,
    connect_db,
    User,
#     Book,
#     UserBook,
#     Comment,
#     Club,
#     ClubMembers,
#     Message,
)

from routes import auth_route, user_route, book_route, club_route, den_route, forum_route

# Load environmental variables file
load_dotenv()

# Import Environmental Variables
production_db = os.environ.get("DB_URI")
# If local database should have the format: "postgresql:///<dbname>"
testrun = os.environ.get("TESTRUN")  # True or False
secret_code = os.environ.get("SECRETE_KEY")
api_key = os.environ.get("GOOGLE_API_KEY")

# Setup Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = secret_code
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["GOOGLE_API_KEY"] = api_key
debug = DebugToolbarExtension(app)

# Detect if testing environmental variable is set to True
if not testrun:
    app.config["SQLALCHEMY_DATABASE_URI"] = production_db
    connect_db(app)

# In case of running the app on python terminal
if __name__ == "__main__":
    app.app_context().push()


@app.before_request
def load_user():
    """If user login id found in session, load current user to Flask global."""

    if "CURRENT_USER" in session:
        g.user = db.get_or_404(User, session["CURRENT_USER"])

    else:
        g.user = None

"""
Blueprint routes
"""
app.register_blueprint(auth_route)
app.register_blueprint(user_route, url_prefix='/user')
app.register_blueprint(book_route)
app.register_blueprint(club_route, url_prefix='/clubs')
app.register_blueprint(den_route, url_prefix='/den')
app.register_blueprint(forum_route, url_prefix='/forum')

"""
# View functions
"""

@app.route("/", methods=["GET"])
def homepage():
    """View Function for the portal homepage."""
    # if g.user:
    #     return redirect(url_for("den_route.user_den_view"))
    return render_template("homepage.html")
