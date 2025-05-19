from flask import Flask, render_template as render
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from datetime import datetime as dt

DB_NAME = 'website.db'
DB_PATH = Path(__file__).parent / DB_NAME

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))

    def __repr__(self):
        return self.title

@app.route('/')
@app.route('/home')
def index():
    notes = Note.query.all()
    return render('index.html', notes=notes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print(' * Database is active!')
    app.run(debug=True, port=5555, host='0.0.0.0')