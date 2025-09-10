from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # The new import for hashing
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # Initialize Bcrypt

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # The new password field to store the hashed password
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'


    

@app.route('/', methods=['GET'])
def index():
    students= Student.query.order_by(Student.name).all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name'].lower().strip()
        email = request.form['email'].lower()
        plain_password = request.form['password'] # Get the plain-text password from the form
        hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')
        new_student = Student(name=name, email=email, password=hashed_password)

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occured: {e}"


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return render_template('update.html', student=student)

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred: {e}"

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)