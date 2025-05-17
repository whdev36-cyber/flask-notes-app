from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')