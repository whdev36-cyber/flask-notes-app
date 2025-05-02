from flask import Flask

import os
import dotenv
dotenv.load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    from . import views
    from . import auth

    return app

import secrets
print(secrets.token_hex())