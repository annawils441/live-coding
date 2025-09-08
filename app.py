from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Welcome to the Homepage</h1>'

@app.route('/register')
def register_student():
    return 'Register Page'

if __name__ == '__main__':
    app.run(debug=True)