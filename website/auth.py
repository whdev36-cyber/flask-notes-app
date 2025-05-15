from flask import Blueprint, render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
import logging

from website.forms import LoginForm, RegisterForm
from website.models import User
from website import db

auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

def redirect_authenticated_users():
    """Helper function to redirect already logged-in users"""
    if current_user.is_authenticated:
        flash('You are already logged in!', 'info')
        return redirect(url_for('views.home'))
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is already authenticated
    if (redirect := redirect_authenticated_users()):
        return redirect

    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            
            if not user or not check_password_hash(user.password, form.password.data):
                flash('Invalid email or password', 'error')
                logger.warning(f'Failed login attempt for email: {form.email.data}')
                return render_template('login.html', form=form)
                
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully!', 'success')
            
            # Safe redirect handling
            next_page = request.args.get('next')
            if next_page and not next_page.startswith('/'):
                next_page = None
            return redirect(next_page or url_for('views.home'))
            
        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            flash('An error occurred during login', 'error')
    
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect if user is already authenticated
    if (redirect := redirect_authenticated_users()):
        return redirect

    form = RegisterForm()
    
    if form.validate_on_submit():
        try:
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered', 'error')
                return render_template('register.html', form=form)
                
            new_user = User(
                email=form.email.data,
                name=form.name.data,
                password=generate_password_hash(
                    form.password.data,
                    method='scrypt',
                    salt_length=16
                )
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            logger.info(f'New user registered: {form.email.data}')
            return redirect(url_for('auth.login'))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f'Registration error: {str(e)}')
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('You have been logged out successfully.', 'success')
    except Exception as e:
        logger.error(f'Logout error: {str(e)}')
        flash('Logout failed. Please try again.', 'error')
    
    return redirect(url_for('auth.login'))