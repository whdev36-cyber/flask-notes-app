from flask import Flask, render_template as render, redirect, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from datetime import datetime as dt
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
import os
from werkzeug.security import generate_password_hash
import dotenv

dotenv.load_dotenv()

DB_NAME = 'website.db'
DB_PATH = Path(__file__).parent / DB_NAME

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)

    def __repr__(self):
        return self.email
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, default=lambda: dt.now().strftime("%Y-%m-%d %H:%M:%S"))
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.title

class RegisterForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Create password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('This email is already registered.')

@app.route('/')
@app.route('/home')
def index():
    notes = Note.query.all()
    return render('index.html', notes=notes)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index')) # TODO: Change to login
    return render('register.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(' * Database is active!')
    app.run(debug=True, port=5555, host='0.0.0.0')