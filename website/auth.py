from flask import Blueprint, render_template, flash, redirect, url_for
from website.forms import LoginForm, RegisterForm
from .models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data, name=form.name.data)
        new_user.password = generate_password_hash(password=form.password.data, method='scrypt')
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! Please log in.', category='success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)