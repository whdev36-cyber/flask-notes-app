from flask import Flask, render_template as render, flash, request, url_for, redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError
from wtforms import EmailField, PasswordField, SubmitField, StringField, TextAreaField
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from pathlib import Path
import os

# Initialize flask app
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')