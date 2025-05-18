from flask import Flask, render_template as render
import json
import os
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

DB_NAME = 'website.db'
DB_PATH = Path(__file__).parent / DB_NAME

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def index():
    with open('data/notes.json', 'r') as f:
        notes = json.load(f)
    return render('index.html', notes=notes)

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')