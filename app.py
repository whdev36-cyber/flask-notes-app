from flask import Flask, render_template as render, flash, request, url_for, redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError
from wtforms import EmailField, PasswordField, SubmitField, StringField, TextAreaField
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import dotenv
import os

dotenv.load_dotenv() # load virtual environment from .env
DB_NAME = 'note.db' # database name
DB_PATH = Path(__file__).parent/DB_NAME # database path

# Initialize flask app
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)

# Configure Flask-Login extension
login_manager.login_message = ''
login_manager.login_view = ''
login_manager.login_message_category = ''

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Set the user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
