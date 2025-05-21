from flask import Flask, render_template as render, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, TextAreaField
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from pathlib import Path
from datetime import datetime as dt
import os
import dotenv
# import logging

# Load environment variables
dotenv.load_dotenv()

# Configuration
DB_NAME = 'website.db'
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / DB_NAME

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Login manager settings
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'

# # Enable logging
# logging.basicConfig(level=logging.INFO)

# Models
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
    title = db.Column(db.String(150), nullable=False, default=lambda: dt.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.title

# Forms
class RegisterForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Create Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data.strip().lower()).first():
            raise ValidationError('This email is already registered.')

class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=1, max=150), DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

# Routes
@app.route('/')
@app.route('/home')
def index():
    users = User.query.all()
    return render('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(email=form.email.data.strip().lower(), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created successfully. Please log in.', category='success')
        return redirect(url_for('login'))
    return render('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', category='success')
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid email or password.', category='danger')
    return render('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('login'))

@app.route('/create/note', methods=['POST', 'GET'])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_note)
        db.session.commit()
        flash('Note created successfully!', category='success')
        return redirect(url_for('index'))
    return render('note_form.html', form=form, title='Create Note')

@app.route('/update/note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        flash('Unauthorized access to update this note.', category='danger')
        return redirect(url_for('index'))
    
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Note updated successfully!', category='success')
        return redirect(url_for('index'))
    return render('note_form.html', form=form, title='Update Note')

@app.route('/delete/note/<note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        flash('Unauthorized action.', category='danger')
        return redirect(url_for('index'))
    
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', category='info')
    return redirect(url_for('index'))

# Run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # logging.info(' * Database initialized.')
        print(' * Database initialized.')
    app.run(debug=True, port=5555, host='0.0.0.0')
