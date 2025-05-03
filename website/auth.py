from flask import Blueprint, render_template, flash, redirect, url_for, request
from website.forms import LoginForm, RegisterForm
from .models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash('You already in the system!')
        return redirect(url_for('views.home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Logged in successfully!', category='success')
                next_page = request.args.get('next', '')
                return redirect(next_page or url_for('views.home'))
            else:
                flash('Invalid email or password, please try again!', category='error')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        flash('You already in the system!')
        return redirect(url_for('views.home'))
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(email=form.email.data, name=form.name.data,
                password=generate_password_hash(password=form.password.data, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! Please log in.', category='success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)