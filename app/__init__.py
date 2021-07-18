from flask import Flask

flask_app = Flask(__name__)
flask_app.secret_key = '266091f8165a9b3870bf9ba2'

from app import routes
