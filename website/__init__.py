from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
import dotenv
dotenv.load_dotenv()

DB_NAME = 'website.db'

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    from . import views
    from . import auth

    app.register_blueprint(views.views, url_prefix='/')
    app.register_blueprint(auth.auth, url_prefix='/')

    from . import models
    from .models import User, Note
    create_db(app)

    return app

def create_db(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print(' * Database has been created!') # for testing purposes
    else:
        print(' * Database already exists!')