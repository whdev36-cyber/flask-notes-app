from flask import Flask, render_template as render
import json
import os
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from datetime import datetime as dt

DB_NAME = 'website.db'
DB_PATH = Path(__file__).parent / DB_NAME

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, default=dt.now())
    content = db.Column(db.Text(), nullable=False)

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