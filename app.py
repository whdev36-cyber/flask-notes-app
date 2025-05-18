from flask import Flask, render_template as render
import json
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/home')
def index():
    with open('data/notes.json', 'r') as f:
        notes = json.load(f)
    return render('index.html', notes=notes)

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')