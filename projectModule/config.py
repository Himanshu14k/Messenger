# Statement for enabling the development environment
from flask import Flask
from projectModule import app
import os
from flask_mail import Mail
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.urandom(32)

# Secret key for signing cookies
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# send mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# CORS resources configuration
cors_config = {
    "origins": ["http://localhost:5000", "https://fornaxbackend.herokuapp.com/"],
    "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
    "allow_headers": ["Authorization"]
}
