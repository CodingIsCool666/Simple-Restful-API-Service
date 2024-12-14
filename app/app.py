from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Database configuration from environment variable
load_dotenv()
DATABASE_HOST=os.getenv('DATABASE_HOST')
DATABASE_PORT=os.getenv('DATABASE_PORT')
DATABASE_URL = f'{DATABASE_HOST}:{DATABASE_PORT}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy ORM
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'major': self.major
        }

# Endpoint to get all students
@app.route('/api/student', methods=['GET'])
def get_student():
    try:
        students = Student.query.all()
        if students:
            student_list = [student.to_dict() for student in students]
            return jsonify(student_list), 200
        else:
            return "No students found", 404
    except Exception as e:
        return str(e), 500

# Endpoint to add a student
@app.route('/api/student', methods=['POST'])
def add_student():
    try:
        student_data = request.get_json()
        name = student_data.get('name')
        age = student_data.get('age')
        major = student_data.get('major')
        if not all([name, age, major]):
            return "Missing required fields", 400

        new_student = Student(name=name, age=age, major=major)
        db.session.add(new_student)
        db.session.commit()
        return "Student added successfully", 201

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add initial data if the table is empty
        if Student.query.count() == 0:
            initial_students = [
                Student(name="Alice", age=20, major="Physics"),
                Student(name="Bob", age=21, major="Mathematics"),
                Student(name="Charlie", age=22, major="Computer Science"),
                Student(name="Diana", age=23, major="Biology"),
            ]
            db.session.bulk_save_objects(initial_students)
            db.session.commit()

    app.run(host='0.0.0.0', port=8888)
