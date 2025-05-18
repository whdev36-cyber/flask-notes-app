from flask import Flask, render_template as render

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/home')
def index():
    return render('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')