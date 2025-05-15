from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path
import os
import dotenv
import logging

# Initialize environment
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_NAME = 'website.db'
DB_PATH = Path(__file__).parent / DB_NAME

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-fallback-key')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_DISABLED = False

def register_blueprints(app):
    """Register all application blueprints"""
    from website.views import views
    from website.auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

def setup_login_manager(app):
    """Configure Flask-Login extension"""
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from website.models import User
        return User.query.get(int(user_id))

def create_database(app):
    """Create database tables if they don't exist"""
    with app.app_context():
        if not DB_PATH.exists():
            try:
                db.create_all()
                logger.info('* Database created successfully at %s', DB_PATH)
                
            except Exception as e:
                logger.error(' * Database creation failed: %s', e)
                raise
        else:
            logger.info(' * Database already exists at %s', DB_PATH)

def create_app(config_class=Config):
    """Application factory function"""
    # Initialize Flask app
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    setup_login_manager(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create database
    create_database(app)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app